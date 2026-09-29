import os
import sys
import re
import uuid
import zipfile
from typing import List, Dict, Tuple, Callable, Optional

# 優先將本地、PyInstaller 執行檔目錄或 _MEIPASS 中的 ffmpeg_bin 加入 PATH
search_paths = []
if hasattr(sys, '_MEIPASS'):
    search_paths.append(os.path.join(sys._MEIPASS, 'ffmpeg_bin'))

if getattr(sys, 'frozen', False):
    search_paths.append(os.path.join(os.path.dirname(sys.executable), 'ffmpeg_bin'))

base_dir = os.path.dirname(os.path.abspath(__file__))
search_paths.append(os.path.join(base_dir, 'ffmpeg_bin'))

for p in search_paths:
    if os.path.exists(p):
        os.environ["PATH"] = p + os.pathsep + os.environ.get("PATH", "")
        break

# 備用嘗試 static_ffmpeg
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except Exception:
    pass

import yt_dlp

AUDIO_EXTENSIONS = ('.mp3', '.mp4', '.m4a', '.wav', '.flac', '.aac', '.ogg', '.mkv', '.webm')
NUMBER_PATTERN = re.compile(r'^(\d{1,4})(?:[\s_\-\.]+|\s*-\s*)(.+)$')

def natural_sort_key(s: str):
    """自然排序（例如 1, 2, 10 不會被排成 1, 10, 2）"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def clean_media_title(filename: str) -> Tuple[str, str]:
    """分離出不帶既有編號前綴的純檔名與副檔名"""
    stem, ext = os.path.splitext(filename)
    m = NUMBER_PATTERN.match(stem)
    if m:
        return m.group(2).strip(), ext
    return stem.strip(), ext

def find_existing_duplicate(folder_path: str, title: str, target_ext: str) -> Optional[Tuple[str, str]]:
    """
    檢查資料夾中是否已有相同歌曲 (不論有無前綴 001 - 或後綴 (1))
    回傳 (檔名, 完整路徑) 或 None
    """
    if not os.path.exists(folder_path):
        return None

    clean_target = sanitize_filename(title).strip().lower()
    clean_target_no_dup = re.sub(r'\s*\(\d+\)$', '', clean_target).strip()

    try:
        filenames = os.listdir(folder_path)
    except Exception:
        return None

    for f in filenames:
        full_path = os.path.join(folder_path, f)
        if not os.path.isfile(full_path):
            continue

        stem, ext = os.path.splitext(f)
        if ext.lower() != target_ext.lower():
            continue

        clean_f, _ = clean_media_title(f)
        clean_f_lower = clean_f.strip().lower()
        clean_f_no_dup = re.sub(r'\s*\(\d+\)$', '', clean_f_lower).strip()

        # 比對名稱 (精準比對，或去除結尾 (1) 後比對)
        if clean_f_lower == clean_target or clean_f_no_dup == clean_target_no_dup:
            return f, full_path

    return None

def get_unique_suffix_stem(folder_path: str, prefix_str: str, safe_title: str, target_ext: str) -> Tuple[str, str]:
    """
    產生加上 (1), (2)... 後綴的唯一檔名，避免覆蓋
    回傳 (產生的 stem 名稱, 完整路徑)
    """
    counter = 1
    while True:
        candidate_stem = f"{prefix_str}{safe_title} ({counter})"
        candidate_filename = f"{candidate_stem}{target_ext}"
        candidate_path = os.path.join(folder_path, candidate_filename)
        if not os.path.exists(candidate_path):
            return candidate_stem, candidate_path
        counter += 1

def get_removable_drives() -> List[str]:
    """獲取目前 Windows 連接的所有隨身碟 (USB Removable Drives)"""
    drives = []
    try:
        import ctypes, string
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drive_path = f"{letter}:\\"
                # DRIVE_REMOVABLE == 2
                if ctypes.windll.kernel32.GetDriveTypeW(drive_path) == 2:
                    drives.append(drive_path)
            bitmask >>= 1
    except Exception:
        pass
    return drives

def check_folder_numbering(folder_path: str) -> Dict:
    """
    檢查指定資料夾（如隨身碟或自選資料夾）中的音訊/影片檔案是否符合 001, 002... 編號格式
    """
    if not os.path.exists(folder_path):
        return {
            'exists': False,
            'status': 'empty',
            'total_files': 0,
            'un_numbered_files': [],
            'numbered_files': [],
            'next_number': 1
        }

    try:
        files = [
            f for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(AUDIO_EXTENSIONS)
        ]
    except Exception:
        files = []

    if not files:
        return {
            'exists': True,
            'status': 'empty',
            'total_files': 0,
            'un_numbered_files': [],
            'numbered_files': [],
            'next_number': 1
        }

    numbered_files = []
    un_numbered_files = []

    for f in files:
        stem, _ = os.path.splitext(f)
        m = NUMBER_PATTERN.match(stem)
        if m:
            num = int(m.group(1))
            numbered_files.append((num, f))
        else:
            un_numbered_files.append(f)

    if len(un_numbered_files) == 0:
        # 所有現有檔案皆具備編號格式
        max_num = max(num for num, _ in numbered_files) if numbered_files else 0
        return {
            'exists': True,
            'status': 'already_numbered',
            'total_files': len(files),
            'un_numbered_files': [],
            'numbered_files': numbered_files,
            'next_number': max_num + 1
        }
    else:
        # 部分或全部檔案尚未編號
        return {
            'exists': True,
            'status': 'not_numbered',
            'total_files': len(files),
            'un_numbered_files': un_numbered_files,
            'numbered_files': numbered_files,
            'next_number': len(files) + 1
        }

def rename_folder_files_to_numbered(folder_path: str, start_number: int = 1) -> int:
    """
    將資料夾中現有的音訊/影片檔案依照自然排序重新命名為 001 - 原檔名.mp3...
    使用二階段更名，避免檔名衝突
    回傳下一個接續的號碼
    """
    if not os.path.exists(folder_path):
        return start_number

    files = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(AUDIO_EXTENSIONS)
    ]
    if not files:
        return start_number

    files.sort(key=natural_sort_key)

    # 第一階段：更名為臨時唯一檔名，避免互換碰撞
    temp_pairs = []
    for f in files:
        old_path = os.path.join(folder_path, f)
        _, ext = os.path.splitext(f)
        temp_name = f"_tmp_{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join(folder_path, temp_name)
        os.rename(old_path, temp_path)
        temp_pairs.append((temp_path, f))

    # 第二階段：正規命名為 001 - 純檔名.ext
    curr_num = start_number
    for temp_path, original_f in temp_pairs:
        clean_title, ext = clean_media_title(original_f)
        new_name = f"{curr_num:03d} - {clean_title}{ext}"
        new_path = os.path.join(folder_path, new_name)
        os.rename(temp_path, new_path)
        curr_num += 1

    return curr_num

def format_duration(seconds: Optional[int]) -> str:
    """將秒數格式化為 mm:ss 或 hh:mm:ss"""
    if not seconds:
        return "未知長度"
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def sanitize_filename(name: str) -> str:
    """移除非法檔名字元"""
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def parse_youtube_urls(raw_input: str) -> List[str]:
    """從輸入文字中提取所有網址（一行一個，自動去除前後空白）"""
    urls = []
    for line in raw_input.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "http://" in line or "https://" in line or "youtube.com" in line or "youtu.be" in line:
            if not line.startswith("http"):
                line = "https://" + line
            urls.append(line)
    return urls

def extract_single_url_info(url: str) -> List[Dict]:
    """
    解析單一網址（可以是單曲或播放清單）
    回傳提取到的歌曲清單
    """
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 30,
        'geo_bypass': True,
        'retries': 10,
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android', 'mweb', 'web']
            }
        },
        'js_runtimes': {'node': {}},
        'remote_components': ['ejs:github'],
    }

    items = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            if not info:
                return items

            # 如果是播放清單或合輯
            if 'entries' in info and info['entries'] is not None:
                for e in info['entries']:
                    if not e:
                        continue
                    v_id = e.get('id')
                    v_url = e.get('url')
                    if not v_url or not v_url.startswith('http'):
                        v_url = f"https://www.youtube.com/watch?v={v_id}" if v_id else url

                    thumb = ""
                    if e.get('thumbnails'):
                        thumb = e['thumbnails'][-1].get('url', '')
                    elif v_id:
                        thumb = f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg"

                    items.append({
                        'id': v_id or str(hash(v_url)),
                        'url': v_url,
                        'title': e.get('title') or '未知標題',
                        'uploader': e.get('uploader') or e.get('channel') or '未知創作者',
                        'duration': e.get('duration'),
                        'duration_str': format_duration(e.get('duration')),
                        'thumbnail': thumb,
                        'selected': True,
                        'status': '等待中',
                        'progress': 0,
                        'file_path': None,
                        'error': None
                    })
            else:
                # 單一影片
                v_id = info.get('id')
                v_url = info.get('webpage_url') or url
                thumb = info.get('thumbnail') or (f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg" if v_id else "")

                items.append({
                    'id': v_id or str(hash(v_url)),
                    'url': v_url,
                    'title': info.get('title') or '未知標題',
                    'uploader': info.get('uploader') or info.get('channel') or '未知創作者',
                    'duration': info.get('duration'),
                    'duration_str': format_duration(info.get('duration')),
                    'thumbnail': thumb,
                    'selected': True,
                    'status': '等待中',
                    'progress': 0,
                    'file_path': None,
                    'error': None
                })
        except Exception as ex:
            items.append({
                'id': str(hash(url)),
                'url': url,
                'title': f"解析錯誤",
                'uploader': "未知",
                'duration': None,
                'duration_str': "未知",
                'thumbnail': "",
                'selected': False,
                'status': '解析失敗',
                'progress': 0,
                'file_path': None,
                'error': str(ex)
            })
    return items

def extract_all_metadata(urls: List[str], callback: Optional[Callable[[int, int, str], None]] = None) -> List[Dict]:
    """
    批次解析多個網址（支援多個影片與多個播放清單混合）
    回傳去重後的完整歌曲清單
    """
    all_items = []
    seen_ids = set()

    for idx, url in enumerate(urls, 1):
        if callback:
            callback(idx, len(urls), url)
        items = extract_single_url_info(url)
        for item in items:
            unique_key = item['id'] or item['url']
            if unique_key not in seen_ids:
                seen_ids.add(unique_key)
                all_items.append(item)

    return all_items

class YTDLCommandLogger:
    def __init__(self, log_callback: Optional[Callable[[str], None]] = None):
        self.log_callback = log_callback

    def debug(self, msg: str):
        if not self.log_callback:
            return
        m = msg.strip()
        # 過濾極度冗長的內部 debug，保留重要轉檔、下載、合併訊息
        if m and not m.startswith('[debug] Encodings') and not m.startswith('[debug] [') and (
            '[download]' in m or '[ExtractAudio]' in m or '[Merger]' in m or 
            '[Metadata]' in m or '[ThumbnailsConvertor]' in m or 'Destination:' in m
        ):
            self.log_callback(m)

    def info(self, msg: str):
        if self.log_callback:
            m = msg.strip()
            if m:
                self.log_callback(m)

    def warning(self, msg: str):
        if self.log_callback:
            self.log_callback(f"[yt-dlp 警告] {msg.strip()}")

    def error(self, msg: str):
        if self.log_callback:
            self.log_callback(f"[yt-dlp 錯誤] {msg.strip()}")

def download_media(
    url: str,
    output_dir: str,
    format_type: str = "mp3",  # "mp3" 或 "mp4"
    quality: str = "320",      # mp3: 320, 256, 192, 128; mp4: best, 1080, 720, 480, 360
    embed_thumbnail: bool = True,
    embed_metadata: bool = True,
    progress_hook: Optional[Callable[[Dict], None]] = None,
    number_prefix: Optional[str] = None,  # 例如 "001 - "
    log_callback: Optional[Callable[[str], None]] = None,
    custom_filename: Optional[str] = None, # 自訂完整檔名 (不含副檔名)
    overwrite: bool = True,
    cancel_check: Optional[Callable[[], bool]] = None
) -> str:
    """
    下載媒體並轉檔為 MP3 或 MP4
    可指定數字前綴 (如 "001 - ")、自訂檔名、是否覆蓋、即時日誌與取消檢查
    回傳產生的檔案路徑
    """
    os.makedirs(output_dir, exist_ok=True)
    prefix_str = number_prefix if number_prefix else ""
    
    if custom_filename:
        outtmpl = os.path.join(output_dir, f"{custom_filename}.%(ext)s")
    else:
        outtmpl = os.path.join(output_dir, f"{prefix_str}%(title)s.%(ext)s")

    postprocessors = []

    if format_type.lower() == "mp3":
        format_spec = 'bestaudio/best'
        postprocessors.append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': quality,
        })
        if embed_metadata:
            postprocessors.append({'key': 'FFmpegMetadata'})
        if embed_thumbnail:
            postprocessors.append({'key': 'EmbedThumbnail'})

        ydl_opts = {
            'format': format_spec,
            'outtmpl': outtmpl,
            'postprocessors': postprocessors,
            'writethumbnail': embed_thumbnail,
            'overwrites': overwrite,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 3,
            'socket_timeout': 30,
            'geo_bypass': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'mweb', 'web']
                }
            },
            'no_warnings': True,
            'js_runtimes': {'node': {}},
            'remote_components': ['ejs:github'],
        }
        target_ext = '.mp3'

    else:
        # MP4 模式
        if quality.lower() == "best" or not quality.isdigit():
            format_spec = 'bv*[vcodec^=avc]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b'
        else:
            format_spec = f'bv*[height<={quality}][vcodec^=avc]+ba[ext=m4a]/b[height<={quality}][ext=mp4]/bv*[height<={quality}]+ba/b'

        if embed_metadata:
            postprocessors.append({'key': 'FFmpegMetadata'})

        ydl_opts = {
            'format': format_spec,
            'outtmpl': outtmpl,
            'merge_output_format': 'mp4',
            'postprocessors': postprocessors,
            'overwrites': overwrite,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 3,
            'socket_timeout': 30,
            'geo_bypass': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'mweb', 'web']
                }
            },
            'no_warnings': True,
            'js_runtimes': {'node': {}},
            'remote_components': ['ejs:github'],
        }
        target_ext = '.mp4'

    if log_callback:
        ydl_opts['logger'] = YTDLCommandLogger(log_callback)
        ydl_opts['quiet'] = False
    else:
        ydl_opts['quiet'] = True

    # 內部進度與取消攔截勾點
    def _internal_hook(d):
        if cancel_check and cancel_check():
            raise Exception("下載已被使用者取消")
        if progress_hook:
            progress_hook(d)
        if log_callback and d.get('status') == 'downloading':
            pct = d.get('_percent_str', '').strip()
            speed = d.get('_speed_str', '').strip()
            eta = d.get('_eta_str', '').strip()
            if pct:
                log_callback(f"[下載進度] {pct} | 速度: {speed} | 剩餘: {eta}")
        elif log_callback and d.get('status') == 'finished':
            log_callback("[轉檔中] 串流下載完成，正在由 FFmpeg 轉檔與注入標籤...")

    ydl_opts['progress_hooks'] = [_internal_hook]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if cancel_check and cancel_check():
            raise Exception("下載已被使用者取消")
            
        info = ydl.extract_info(url, download=True)
        title = info.get('title', 'media')
        safe_title = sanitize_filename(title)

        if custom_filename:
            expected_filename = f"{custom_filename}{target_ext}"
        else:
            expected_filename = f"{prefix_str}{safe_title}{target_ext}"
            
        expected_path = os.path.join(output_dir, expected_filename)
        if os.path.exists(expected_path):
            return expected_path

        candidates = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(target_ext)]
        if candidates:
            candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
            return candidates[0]

        return expected_path

# 向後相容別名
download_audio_to_mp3 = download_media

def create_zip_archive(file_paths: List[str], zip_output_path: str) -> str:
    """將多個檔案壓縮成一個 ZIP 壓縮檔"""
    with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in file_paths:
            if os.path.exists(f):
                zipf.write(f, arcname=os.path.basename(f))
    return zip_output_path
