# -*- coding: utf-8 -*-
"""
StreamForge 播放清單格式處理核心模組 (StreamForge Playlist - SFPL)
支援格式：
  1. StreamForge 專屬歌單 (*.sfpl, application/x-streamforge-playlist)
  2. 標準 JSON 歌單 (*.json)
  3. M3U / M3U8 擴展播放清單 (*.m3u8, *.m3u)
  4. 純文字網址清單 (*.txt)
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Tuple, Optional

SFPL_FORMAT_SIGNATURE = "StreamForgePlaylist"
SFPL_CURRENT_VERSION = "1.1"


def create_sfpl_data(songs: List[Dict], playlist_name: str = "StreamForge 播放清單", extra_settings: Optional[Dict] = None) -> Dict:
    """
    將歌曲清單轉換為標準 SFPL 字典結構
    """
    now_str = datetime.now().astimezone().isoformat(timespec="seconds")
    
    clean_tracks = []
    for s in songs:
        track = {
            "id": s.get("id", ""),
            "title": s.get("title", "未知曲目"),
            "url": s.get("url", ""),
            "uploader": s.get("uploader", "未知頻道"),
            "duration": s.get("duration", 0),
            "duration_str": s.get("duration_str", "00:00"),
            "thumbnail": s.get("thumbnail", ""),
            "selected": bool(s.get("var").get() if "var" in s else s.get("selected", True)),
        }
        clean_tracks.append(track)

    sfpl_data = {
        "format": SFPL_FORMAT_SIGNATURE,
        "version": SFPL_CURRENT_VERSION,
        "generator": "StreamForge v1.1.0",
        "created_at": now_str,
        "playlist_name": playlist_name,
        "total_tracks": len(clean_tracks),
        "settings": extra_settings or {},
        "tracks": clean_tracks,
    }
    return sfpl_data


def save_playlist(file_path: str, songs: List[Dict], playlist_name: str = "StreamForge 播放清單", extra_settings: Optional[Dict] = None) -> Tuple[bool, str]:
    """
    儲存播放清單到指定檔案。依附檔名自動決定格式：
    - .sfpl / .json : SFPL 結構 JSON
    - .m3u / .m3u8  : 擴展 M3U 格式
    - .txt          : 純文字網址每行一筆
    """
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in (".sfpl", ".json", ""):
            # 預設儲存為 SFPL 格式
            data = create_sfpl_data(songs, playlist_name, extra_settings)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, f"成功儲存 SFPL 歌單（共 {len(songs)} 首曲目）"

        elif ext in (".m3u", ".m3u8"):
            lines = ["#EXTM3U", f"#EXTENC: UTF-8", f"#PLAYLIST: {playlist_name}"]
            for s in songs:
                duration = int(s.get("duration", 0) or 0)
                artist = s.get("uploader", "Unknown Artist")
                title = s.get("title", "Unknown Title")
                url = s.get("url", "")
                if url:
                    lines.append(f"#EXTINF:{duration},{artist} - {title}")
                    lines.append(url)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            return True, f"成功儲存 M3U 歌單（共 {len(songs)} 首曲目）"

        elif ext == ".txt":
            lines = [f"# StreamForge Playlist Export: {playlist_name}", f"# Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ""]
            for i, s in enumerate(songs, 1):
                url = s.get("url", "").strip()
                if url:
                    lines.append(f"# {i}. {s.get('title', '')} ({s.get('uploader', '')})")
                    lines.append(url)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            return True, f"成功儲存純文字網址清單（共 {len(songs)} 首曲目）"

        else:
            # 未知副檔名預設以 SFPL 儲存
            data = create_sfpl_data(songs, playlist_name, extra_settings)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, f"成功儲存歌單（共 {len(songs)} 首曲目）"

    except Exception as e:
        return False, f"儲存播放清單失敗：{str(e)}"


def load_playlist(file_path: str) -> Tuple[bool, List[Dict], str]:
    """
    從指定檔案載入播放清單。
    支援 .sfpl, .json, .m3u, .m3u8, .txt
    回傳 (成功與否, 曲目列表, 提示訊息)
    """
    if not os.path.exists(file_path):
        return False, [], f"找不到檔案：{file_path}"

    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        # 嘗試讀取內容
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read().strip()

        if not content:
            return False, [], "檔案內容為空！"

        # 優先嘗試以 JSON / SFPL 解析
        if ext in (".sfpl", ".json") or content.startswith("{"):
            try:
                data = json.loads(content)
                if isinstance(data, dict):
                    # SFPL 或客製 JSON
                    tracks_raw = data.get("tracks", [])
                    if not tracks_raw and "songs" in data:
                        tracks_raw = data.get("songs", [])
                    if not tracks_raw and "items" in data:
                        tracks_raw = data.get("items", [])

                    tracks = []
                    for t in tracks_raw:
                        if isinstance(t, dict) and t.get("url"):
                            track = {
                                "id": t.get("id") or extract_youtube_id(t["url"]),
                                "title": t.get("title") or t["url"],
                                "url": t["url"],
                                "uploader": t.get("uploader", "未知頻道"),
                                "duration": t.get("duration", 0),
                                "duration_str": t.get("duration_str", "00:00"),
                                "thumbnail": t.get("thumbnail", ""),
                                "selected": t.get("selected", True),
                            }
                            tracks.append(track)
                        elif isinstance(t, str) and t.startswith("http"):
                            tracks.append(_create_basic_track(t))

                    format_tag = data.get("format", "JSON")
                    version_tag = data.get("version", "1.0")
                    return True, tracks, f"成功解析 {format_tag} v{version_tag} 歌單，共 {len(tracks)} 首曲目"
                elif isinstance(data, list):
                    # JSON 陣列格式
                    tracks = []
                    for item in data:
                        if isinstance(item, dict) and item.get("url"):
                            tracks.append({
                                "id": item.get("id") or extract_youtube_id(item["url"]),
                                "title": item.get("title", item["url"]),
                                "url": item["url"],
                                "uploader": item.get("uploader", "未知頻道"),
                                "duration": item.get("duration", 0),
                                "duration_str": item.get("duration_str", "00:00"),
                                "thumbnail": item.get("thumbnail", ""),
                                "selected": True,
                            })
                        elif isinstance(item, str) and item.startswith("http"):
                            tracks.append(_create_basic_track(item))
                    return True, tracks, f"成功解析 JSON 歌單陣列，共 {len(tracks)} 首曲目"
            except json.JSONDecodeError:
                pass  # 若不是合法 JSON，接續嘗試 M3U / TXT 解析

        # M3U / M3U8 解析
        if ext in (".m3u", ".m3u8") or content.startswith("#EXTM3U"):
            tracks = []
            current_title = ""
            current_artist = ""
            current_duration = 0

            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("#EXTINF:"):
                    # #EXTINF:213,Artist - Title
                    info = line[8:].strip()
                    parts = info.split(",", 1)
                    try:
                        current_duration = int(float(parts[0]))
                    except Exception:
                        current_duration = 0
                    if len(parts) > 1:
                        raw_title = parts[1].strip()
                        if " - " in raw_title:
                            artist_part, title_part = raw_title.split(" - ", 1)
                            current_artist = artist_part.strip()
                            current_title = title_part.strip()
                        else:
                            current_title = raw_title
                            current_artist = "未知頻道"
                elif not line.startswith("#"):
                    # URL 行
                    url = line
                    mins, secs = divmod(current_duration, 60)
                    dur_str = f"{mins:02d}:{secs:02d}"
                    track = {
                        "id": extract_youtube_id(url),
                        "title": current_title or url,
                        "url": url,
                        "uploader": current_artist or "未知頻道",
                        "duration": current_duration,
                        "duration_str": dur_str,
                        "thumbnail": "",
                        "selected": True,
                    }
                    tracks.append(track)
                    # 重置暫存
                    current_title = ""
                    current_artist = ""
                    current_duration = 0

            return True, tracks, f"成功解析 M3U 歌單，共 {len(tracks)} 首曲目"

        # 純文字網址清單 (.txt) 解析
        lines = content.splitlines()
        tracks = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # 尋找行內是否有 http/https 網址
            match = re.search(r"https?://[^\s]+", line)
            if match:
                url = match.group(0)
                tracks.append(_create_basic_track(url))

        if tracks:
            return True, tracks, f"成功解析純文字網址清單，共 {len(tracks)} 首曲目"

        return False, [], "檔案中未偵測到任何有效的歌曲網址或支援的歌單格式！"

    except Exception as e:
        return False, [], f"解析播放清單時發生例外錯誤：{str(e)}"


def _create_basic_track(url: str) -> Dict:
    """從純網址建立基礎曲目項目"""
    yt_id = extract_youtube_id(url)
    return {
        "id": yt_id or url,
        "title": url,
        "url": url,
        "uploader": "待解析頻道",
        "duration": 0,
        "duration_str": "00:00",
        "thumbnail": "",
        "selected": True,
    }


def extract_youtube_id(url: str) -> str:
    """從 YouTube 網址萃取 11 字元 Video ID"""
    if not url:
        return ""
    m = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|\/|$)", url)
    if m:
        return m.group(1)
    return url
