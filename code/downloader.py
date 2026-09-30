import os
import sys
import re
import time
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
from yt_dlp.utils import DownloadCancelled

AUDIO_FORMATS = ('mp3', 'm4a', 'wav', 'flac', 'aac', 'ogg', 'opus')
VIDEO_FORMATS = ('mp4', 'mkv', 'webm', 'mov', 'avi')
MEDIA_EXTENSIONS = ('.mp3', '.m4a', '.wav', '.flac', '.aac', '.ogg', '.opus', '.mp4', '.mkv', '.webm', '.mov', '.avi', '.wma', '.flv')
AUDIO_EXTENSIONS = MEDIA_EXTENSIONS  # 向後相容
NUMBER_PATTERN = re.compile(r'^(\d{1,4})(?:[\s_\-\.]+|\s*-\s*)(.+)$')

def natural_sort_key(s: str):
    """自然排序（例如 1, 2, 10 不會被排成 1, 10, 2）"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def clean_media_title(filename: str) -> Tuple[str, str]:
    """
    分離出不帶既有編號前綴與重複後綴的純檔名與副檔名
    支援清理多重累贅前綴 (如 "001 - 002 - ", "01. ", "[01] ", "(01) ")
    以及重複後綴 (如 " (1) (1)")，且不會誤切無副檔名標題中的點號。
    """
    name = filename.strip()
    ext = ''
    for cand_ext in MEDIA_EXTENSIONS + ('.webp', '.jpg', '.jpeg', '.png'):
        if name.lower().endswith(cand_ext):
            ext = name[-len(cand_ext):]
            name = name[:-len(cand_ext)].strip()
            break

    stem = name
    prefix_regex = re.compile(r'^(?:\[\d{1,4}\]|\(\d{1,4}\)|\d{1,4}(?:[\s_\-\.]+|\s*-\s*))\s*')
    while True:
        m = prefix_regex.match(stem)
        if m:
            remaining = stem[m.end():].strip()
            if remaining:
                stem = remaining
            else:
                break
        else:
            break

    suffix_regex = re.compile(r'(\s*\(\d+\))+$')
    stem = suffix_regex.sub('', stem).strip()
    return (stem if stem else name), ext

def cleanup_temp_and_thumbnail_files(folder_path: str, stem: str, is_error: bool = False):
    """
    清理下載遺留的暫存檔與多餘的縮圖檔 (.webp, .jpg, .png, .part, .ytdl, .temp)
    - 成功時：清除獨立的 .webp, .jpg, .png 縮圖檔（因為縮圖已內嵌進 MP3/M4A/FLAC 內）
    - 失敗/取消時 (is_error=True)：同時清除 .webp, .jpg, .png, .part, .ytdl, .temp 及 0-byte 媒體檔
    """
    if not os.path.exists(folder_path) or not stem:
        return

    thumb_exts = ('.webp', '.jpg', '.jpeg', '.png')
    temp_exts = ('.part', '.ytdl', '.temp', '.tmp')

    try:
        filenames = os.listdir(folder_path)
    except Exception:
        return

    clean_stem_lower = stem.strip().lower()

    for f in filenames:
        f_lower = f.lower()
        full_path = os.path.join(folder_path, f)

        # 檢查是否屬於此歌曲之產物
        f_stem, f_ext = os.path.splitext(f_lower)
        is_matched = (f_stem == clean_stem_lower) or f_lower.startswith(clean_stem_lower)

        if is_matched:
            # 清除縮圖檔 (無論成功或失敗，都不應在資料夾留下零散的 .webp/.jpg)
            if f_ext in thumb_exts:
                try:
                    os.remove(full_path)
                except Exception:
                    pass

            # 暫存檔清除 (.part, .ytdl, .temp 等)
            if any(f_lower.endswith(te) for te in temp_exts) or '.temp.' in f_lower:
                try:
                    os.remove(full_path)
                except Exception:
                    pass

            # 若失敗或取消，刪除損毀或 0-byte 的檔案
            if is_error:
                try:
                    if os.path.isfile(full_path) and os.path.getsize(full_path) == 0:
                        os.remove(full_path)
                except Exception:
                    pass

def find_existing_duplicate(folder_path: str, title: str, target_ext: str) -> Optional[Tuple[str, str]]:
    """
    檢查資料夾中是否已有相同歌曲 (不論有無前綴 001 - 或後綴 (1))
    回傳 (檔名, 完整路徑) 或 None
    """
    if not os.path.exists(folder_path):
        return None

    clean_target_stem, _ = clean_media_title(title)
    clean_target = sanitize_filename(clean_target_stem).strip().lower()
    clean_target_no_dup = re.sub(r'(\s*\(\d+\))+$', '', clean_target).strip()

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
        clean_f_no_dup = re.sub(r'(\s*\(\d+\))+$', '', clean_f_lower).strip()

        # 比對名稱 (精準比對，或去除結尾 (1) 後比對)
        if clean_f_lower == clean_target or clean_f_no_dup == clean_target_no_dup:
            return f, full_path

    return None

def get_unique_suffix_stem(folder_path: str, prefix_str: str, safe_title: str, target_ext: str) -> Tuple[str, str]:
    """
    產生加上 (1), (2)... 後綴的唯一檔名，避免覆蓋，且去除已存在的 (1) 後綴避免重複累加
    回傳 (產生的 stem 名稱, 完整路徑)
    """
    clean_base, _ = clean_media_title(safe_title)
    counter = 1
    while True:
        candidate_stem = f"{prefix_str}{clean_base} ({counter})"
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
        'skip_download': True,
        'check_formats': False,
        'quiet': True,
        'no_warnings': True,
        'no_color': True,
        'socket_timeout': 10,
        'geo_bypass': True,
        'retries': 2,
        'playlistend': 100,
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
    def __init__(
        self,
        log_callback: Optional[Callable[[str], None]] = None,
        cancel_check: Optional[Callable[[], bool]] = None,
        pause_check: Optional[Callable[[], bool]] = None
    ):
        self.log_callback = log_callback
        self.cancel_check = cancel_check
        self.pause_check = pause_check

    def _check_state(self):
        if self.cancel_check and self.cancel_check():
            raise DownloadCancelled("下載已被使用者取消")
        if self.pause_check:
            while self.pause_check():
                if self.cancel_check and self.cancel_check():
                    raise DownloadCancelled("下載已被使用者取消")
                time.sleep(0.1)

    def debug(self, msg: str):
        self._check_state()
        if not self.log_callback:
            return
        m = msg.strip()
        # 嚴格過濾 raw [download] 數據包，杜絕每秒數百行日誌造成 UI 卡頓！
        # 下載進度已由 _internal_hook 進行 300ms 限頻回報
        if m.startswith('[download]') or m.startswith('[debug]'):
            return
        if m and (
            '[ExtractAudio]' in m or '[Merger]' in m or 
            '[Metadata]' in m or '[ThumbnailsConvertor]' in m or 'Destination:' in m
        ):
            self.log_callback(m)

    def info(self, msg: str):
        self._check_state()
        if self.log_callback:
            m = msg.strip()
            if m and not m.startswith('[download]'):
                self.log_callback(m)

    def warning(self, msg: str):
        self._check_state()
        if self.log_callback:
            self.log_callback(f"[yt-dlp 警告] {msg.strip()}")

    def error(self, msg: str):
        self._check_state()
        if self.log_callback:
            self.log_callback(f"[yt-dlp 錯誤] {msg.strip()}")

def get_ffmpeg_executable() -> str:
    """獲取可用的 ffmpeg 執行檔路徑"""
    for p in search_paths:
        cand = os.path.join(p, "ffmpeg.exe" if sys.platform.startswith("win") else "ffmpeg")
        if os.path.exists(cand):
            return cand
    return "ffmpeg"

def download_media(
    url: str,
    output_dir: str,
    format_type: str = "mp3",  # mp3, m4a, wav, flac, aac, ogg, opus, mp4, mkv, webm, mov, avi
    quality: str = "320",      # 音訊: 320, 256, 192, 128; 視訊: best, 2160, 1440, 1080, 720, 480, 360
    embed_thumbnail: bool = True,
    embed_metadata: bool = True,
    progress_hook: Optional[Callable[[Dict], None]] = None,
    number_prefix: Optional[str] = None,  # 例如 "001 - "
    log_callback: Optional[Callable[[str], None]] = None,
    custom_filename: Optional[str] = None, # 自訂完整檔名 (不含副檔名)
    overwrite: bool = True,
    cancel_check: Optional[Callable[[], bool]] = None,
    pause_check: Optional[Callable[[], bool]] = None
) -> str:
    """
    下載媒體並轉檔為指定音訊 (MP3/M4A/WAV/FLAC/AAC/OGG/OPUS) 或視訊 (MP4/MKV/WEBM/MOV/AVI)
    可指定數字前綴 (如 "001 - ")、自訂檔名、是否覆蓋、即時日誌與取消/暫停檢查
    回傳產生的檔案路徑
    """
    os.makedirs(output_dir, exist_ok=True)
    prefix_str = number_prefix if number_prefix else ""
    
    if custom_filename:
        outtmpl = os.path.join(output_dir, f"{custom_filename}.%(ext)s")
    else:
        outtmpl = os.path.join(output_dir, f"{prefix_str}%(title)s.%(ext)s")

    fmt = format_type.strip().lower()
    postprocessors = []

    # FFmpeg 多核心加速參數 (-threads 0 自動調用 CPU 全核心多線程)
    ffmpeg_multithread_args = {
        'FFmpegExtractAudio': ['-threads', '0'],
        'FFmpegVideoConvertor': ['-threads', '0'],
        'FFmpegMerger': ['-threads', '0'],
        'FFmpegMetadata': ['-threads', '0'],
    }

    if fmt in AUDIO_FORMATS:
        format_spec = 'bestaudio/best'
        target_ext = f'.{fmt}'

        if fmt == 'mp3':
            q_val = quality if quality.isdigit() else '320'
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': q_val,
            })
        elif fmt == 'm4a':
            format_spec = 'bestaudio[ext=m4a]/bestaudio/best'
            q_val = quality if quality.isdigit() else '320'
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': q_val,
            })
        elif fmt == 'wav':
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            })
        elif fmt == 'flac':
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
            })
        elif fmt == 'aac':
            q_val = quality if quality.isdigit() else '320'
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'aac',
                'preferredquality': q_val,
            })
        elif fmt == 'ogg':
            q_val = quality if quality.isdigit() else '320'
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'vorbis',
                'preferredquality': q_val,
            })
        elif fmt == 'opus':
            format_spec = 'bestaudio[ext=opus]/bestaudio/best'
            q_val = quality if quality.isdigit() else '320'
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'opus',
                'preferredquality': q_val,
            })

        if embed_metadata:
            postprocessors.append({'key': 'FFmpegMetadata'})
        if embed_thumbnail and fmt in ('mp3', 'm4a', 'flac', 'ogg'):
            postprocessors.append({'key': 'EmbedThumbnail'})

        ydl_opts = {
            'format': format_spec,
            'outtmpl': outtmpl,
            'postprocessors': postprocessors,
            'writethumbnail': embed_thumbnail and fmt in ('mp3', 'm4a', 'flac', 'ogg'),
            'overwrites': overwrite,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 5,
            'extractor_retries': 5,
            'http_chunk_size': 10485760,
            'socket_timeout': 15,
            'geo_bypass': True,
            'postprocessor_args': ffmpeg_multithread_args,
            'no_warnings': True,
            'js_runtimes': {'node': {}},
            'remote_components': ['ejs:github'],
        }

    else:
        # 視訊模式 (MP4, MKV, WEBM, MOV, AVI)
        target_ext = f'.{fmt}' if fmt in VIDEO_FORMATS else '.mp4'
        merge_fmt = fmt if fmt in VIDEO_FORMATS else 'mp4'

        height_limit = f"[height<={quality}]" if quality.isdigit() else ""
        if fmt == "webm":
            format_spec = f'bv*{height_limit}[vcodec^=vp9]+ba[ext=opus]/bv*{height_limit}+ba/b'
        elif fmt == "mp4":
            format_spec = f'bv*{height_limit}[vcodec^=avc]+ba[ext=m4a]/b{height_limit}[ext=mp4]/bv*{height_limit}+ba/b'
        else:
            format_spec = f'bv*{height_limit}+ba/b{height_limit}/b'

        if embed_metadata:
            postprocessors.append({'key': 'FFmpegMetadata'})

        ydl_opts = {
            'format': format_spec,
            'outtmpl': outtmpl,
            'merge_output_format': merge_fmt,
            'postprocessors': postprocessors,
            'overwrites': overwrite,
            'retries': 10,
            'fragment_retries': 10,
            'file_access_retries': 5,
            'extractor_retries': 5,
            'http_chunk_size': 10485760,
            'socket_timeout': 15,
            'geo_bypass': True,
            'postprocessor_args': ffmpeg_multithread_args,
            'no_warnings': True,
            'js_runtimes': {'node': {}},
            'remote_components': ['ejs:github'],
        }

    ydl_opts['logger'] = YTDLCommandLogger(log_callback, cancel_check, pause_check)
    ydl_opts['quiet'] = False

    # 內部進度、暫停與取消攔截勾點 (帶 300ms 限頻避免介面阻塞)
    last_hook_time = [0.0]

    def _internal_hook(d):
        if cancel_check and cancel_check():
            raise DownloadCancelled("下載已被使用者取消")

        if pause_check:
            while pause_check():
                if cancel_check and cancel_check():
                    raise DownloadCancelled("下載已被使用者取消")
                time.sleep(0.1)

        now = time.time()
        status = d.get('status')
        if status == 'finished':
            if progress_hook:
                progress_hook(d)
            if log_callback:
                log_callback("[轉檔中] 串流下載完成，正在由 FFmpeg 全核心轉檔與注入標籤...")
            return

        if now - last_hook_time[0] < 0.3:
            return
        last_hook_time[0] = now

        if progress_hook:
            progress_hook(d)
        if log_callback and status == 'downloading':
            pct = d.get('_percent_str', '').strip()
            speed = d.get('_speed_str', '').strip()
            eta = d.get('_eta_str', '').strip()
            if pct:
                log_callback(f"[下載進度] {pct} | 速度: {speed} | 剩餘: {eta}")

    def _pp_hook(d):
        if cancel_check and cancel_check():
            raise DownloadCancelled("下載已被使用者取消")
        if pause_check:
            while pause_check():
                if cancel_check and cancel_check():
                    raise DownloadCancelled("下載已被使用者取消")
                time.sleep(0.1)

    ydl_opts['progress_hooks'] = [_internal_hook]
    ydl_opts['postprocessor_hooks'] = [_pp_hook]

    max_retries = 3
    stem_for_cleanup = custom_filename if custom_filename else ""

    for attempt in range(1, max_retries + 1):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if cancel_check and cancel_check():
                    raise DownloadCancelled("下載已被使用者取消")
                    
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'media')
                safe_title = sanitize_filename(title)

                if custom_filename:
                    expected_filename = f"{custom_filename}{target_ext}"
                    stem_for_cleanup = custom_filename
                else:
                    expected_filename = f"{prefix_str}{safe_title}{target_ext}"
                    stem_for_cleanup = f"{prefix_str}{safe_title}"
                    
                expected_path = os.path.join(output_dir, expected_filename)
                final_path = None
                if os.path.exists(expected_path):
                    final_path = expected_path
                else:
                    candidates = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(target_ext)]
                    if candidates:
                        candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                        final_path = candidates[0]
                    else:
                        final_path = expected_path

                # 成功下載後清理孤立的縮圖檔 (.webp / .jpg / .png)，維持音樂資料夾乾淨
                if stem_for_cleanup:
                    cleanup_temp_and_thumbnail_files(output_dir, stem_for_cleanup, is_error=False)

                return final_path

        except DownloadCancelled:
            if stem_for_cleanup:
                cleanup_temp_and_thumbnail_files(output_dir, stem_for_cleanup, is_error=True)
            raise

        except Exception as ex:
            if cancel_check and cancel_check():
                if stem_for_cleanup:
                    cleanup_temp_and_thumbnail_files(output_dir, stem_for_cleanup, is_error=True)
                raise DownloadCancelled("下載已被使用者取消")

            err_str = str(ex)
            # 判斷是否為 YouTube 403 Forbidden、串流被阻擋或暫時性網路中斷
            is_403_or_throttle = any(k in err_str for k in ("403", "Forbidden", "HTTP Error 403", "unable to download video data", "Connection reset", "IncompleteRead"))

            if is_403_or_throttle and attempt < max_retries:
                if log_callback:
                    log_callback(f"⚠️ [防 403 自動重試] 偵測到 YouTube 暫時性串流節流 (HTTP 403)，正在冷卻並自動重試 (第 {attempt}/{max_retries} 次)...")
                
                # 清理本輪失敗的暫存檔案
                if stem_for_cleanup:
                    cleanup_temp_and_thumbnail_files(output_dir, stem_for_cleanup, is_error=True)
                
                # 冷卻退避等候 (1.5s, 3.0s...)
                wait_time = 1.5 * attempt
                start_w = time.time()
                while time.time() - start_w < wait_time:
                    if cancel_check and cancel_check():
                        raise DownloadCancelled("下載已被使用者取消")
                    time.sleep(0.1)
                continue
            else:
                # 已達重試上限或非可重試錯誤
                if stem_for_cleanup:
                    cleanup_temp_and_thumbnail_files(output_dir, stem_for_cleanup, is_error=True)
                raise

# 向後相容別名
download_audio_to_mp3 = download_media

def convert_local_media(
    input_path: str,
    output_path: str,
    target_format: str,
    quality: str = "320",
    log_callback: Optional[Callable[[str], None]] = None,
    cancel_check: Optional[Callable[[], bool]] = None
) -> str:
    """
    使用內建 FFmpeg 將本機現有影音檔案轉檔為指定格式 (完整取代格式工廠)
    支援 MP3, M4A, WAV, FLAC, AAC, OGG, OPUS, MP4, MKV, WEBM, MOV, AVI
    """
    import subprocess
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"找不到來源檔案: {input_path}")

    ffmpeg_bin = get_ffmpeg_executable()
    fmt = target_format.lower().lstrip('.')
    
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    cmd = [ffmpeg_bin, "-y", "-threads", "0", "-i", input_path]

    # 音訊編碼設定
    if fmt == 'mp3':
        q_val = quality if quality.isdigit() else '320'
        cmd.extend(["-vn", "-c:a", "libmp3lame", "-b:a", f"{q_val}k", "-id3v2_version", "3"])
    elif fmt == 'm4a':
        q_val = quality if quality.isdigit() else '320'
        cmd.extend(["-vn", "-c:a", "aac", "-b:a", f"{q_val}k"])
    elif fmt == 'wav':
        cmd.extend(["-vn", "-c:a", "pcm_s16le"])
    elif fmt == 'flac':
        cmd.extend(["-vn", "-c:a", "flac"])
    elif fmt == 'aac':
        q_val = quality if quality.isdigit() else '320'
        cmd.extend(["-vn", "-c:a", "aac", "-b:a", f"{q_val}k"])
    elif fmt == 'ogg':
        q_val = quality if quality.isdigit() else '320'
        cmd.extend(["-vn", "-c:a", "libvorbis", "-b:a", f"{q_val}k"])
    elif fmt == 'opus':
        q_val = quality if quality.isdigit() else '320'
        cmd.extend(["-vn", "-c:a", "libopus", "-b:a", f"{q_val}k"])
    elif fmt == 'mp4':
        cmd.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "22", "-c:a", "aac", "-b:a", "192k"])
    elif fmt == 'mkv':
        cmd.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "22", "-c:a", "aac", "-b:a", "192k"])
    elif fmt == 'webm':
        cmd.extend(["-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0", "-c:a", "libopus", "-b:a", "128k"])
    elif fmt == 'mov':
        cmd.extend(["-c:v", "libx264", "-preset", "fast", "-crf", "22", "-c:a", "aac", "-b:a", "192k"])
    elif fmt == 'avi':
        cmd.extend(["-c:v", "mpeg4", "-qscale:v", "3", "-c:a", "libmp3lame", "-b:a", "192k"])
    else:
        cmd.extend(["-c", "copy"])

    cmd.append(output_path)

    if log_callback:
        log_callback(f"[格式工廠] 正在轉檔: {os.path.basename(input_path)} -> {os.path.basename(output_path)} (格式: {fmt.upper()})")

    startupinfo = None
    if sys.platform.startswith("win"):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        startupinfo=startupinfo,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform.startswith("win") else 0
    )

    _, stderr = proc.communicate()

    if cancel_check and cancel_check():
        proc.kill()
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except Exception:
                pass
        raise Exception("轉檔已被使用者取消")

    if proc.returncode != 0:
        err_msg = stderr.strip().splitlines()[-4:] if stderr else ["未知轉檔錯誤"]
        raise Exception(f"FFmpeg 轉檔失敗 (代碼 {proc.returncode}): {' '.join(err_msg)}")

    if log_callback:
        log_callback(f"🎉 [格式工廠] 轉檔完成: {os.path.basename(output_path)}")

    return output_path

def create_zip_archive(file_paths: List[str], zip_output_path: str) -> str:
    """將多個檔案壓縮成一個 ZIP 壓縮檔"""
    with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in file_paths:
            if os.path.exists(f):
                zipf.write(f, arcname=os.path.basename(f))
    return zip_output_path
