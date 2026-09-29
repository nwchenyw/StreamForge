import os
import sys
import time
import json
import urllib.request
import webbrowser
import threading
import subprocess
from datetime import datetime
from typing import Optional, Callable, List, Dict, Any, Union, Tuple
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import downloader
import i18n

# 設定外觀模式與主題
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ================= 靜態資源路徑解析與圖示設定 =================
def get_asset_path(filename: str) -> str:
    """取得靜態資源路徑 (支援 PyInstaller 打包目錄、assets 子目錄及原始碼模式)"""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    candidates = [
        os.path.join(base_dir, "assets", filename),
        os.path.join(base_dir, filename),
        os.path.join(os.path.dirname(base_dir), "assets", filename),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


def apply_window_icon(window):
    """為指定視窗設定官方 StreamForge 應用程式圖示 (.ico)"""
    ico_path = get_asset_path("app_icon.ico")
    if os.path.exists(ico_path):
        try:
            window.iconbitmap(ico_path)
        except Exception:
            pass


def get_windows_user_downloads_dir() -> str:
    """
    動態精確偵測 Windows 使用者實際的「下載」資料夾路徑。
    支援使用者將下載資料夾轉移至 D:、E: 槽或其他自訂磁碟機之情境。
    優先透過 Windows Shell 註冊表查詢 GUID，次之呼叫 Win32 SHGetKnownFolderPath，最後回退至家目錄。
    """
    if sys.platform == "win32":
        try:
            import winreg
            sub_key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                for guid in ("{374DE290-123F-4565-9164-39C4925E467B}", "{7D83EE9B-2244-4E70-B1F5-5393042AF1E4}", "Downloads"):
                    try:
                        raw_path, _ = winreg.QueryValueEx(key, guid)
                        expanded = os.path.expandvars(raw_path)
                        if expanded and os.path.isdir(expanded):
                            return expanded
                    except OSError:
                        pass
        except Exception:
            pass

        try:
            import ctypes
            from ctypes import wintypes
            class GUID(ctypes.Structure):
                _fields_ = [
                    ("Data1", wintypes.DWORD),
                    ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD),
                    ("Data4", wintypes.BYTE * 8)
                ]
            FOLDERID_Downloads = GUID(0x374DE290, 0x123F, 0x4565, (wintypes.BYTE * 8)(0x91, 0x64, 0x39, 0xC4, 0x92, 0x5E, 0x46, 0x7B))
            path_ptr = ctypes.c_wchar_p()
            if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(FOLDERID_Downloads), 0, None, ctypes.byref(path_ptr)) == 0:
                result = path_ptr.value
                ctypes.windll.ole32.CoTaskMemFree(path_ptr)
                if result and os.path.isdir(result):
                    return result
        except Exception:
            pass

    fallback = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.isdir(fallback):
        return fallback
    return os.path.expanduser("~")

# ================= 設定檔與更新檢查 =================
APP_VERSION = "1.0.0"
GITHUB_REPO = "nwchenyw/StreamForge"
GITHUB_RELEASES_API = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
GITHUB_RELEASES_URL = f"https://github.com/{GITHUB_REPO}/releases"

CONFIG_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "StreamForge")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# ================= 支援多格式與格式工廠定義 =================
AUDIO_FORMAT_OPTIONS = [
    "MP3 (最通用/推薦)",
    "M4A (Apple/AAC)",
    "WAV (無損未壓縮/剪輯)",
    "FLAC (無損高保真)",
    "AAC (現代串流)",
    "OGG (開源多媒體)",
    "OPUS (高質高效)",
]
VIDEO_FORMAT_OPTIONS = [
    "MP4 (通用視訊/推薦)",
    "MKV (高清多軌)",
    "WEBM (網頁高效)",
    "MOV (QuickTime/剪輯)",
    "AVI (傳統視訊)",
]
AUDIO_QUALITIES_LOSSY = [
    "320 kbps (最高品質/推薦)",
    "256 kbps (高質量)",
    "192 kbps (標準)",
    "128 kbps (輕巧)"
]
AUDIO_QUALITIES_LOSSLESS = [
    "無損音質 (Lossless / 原音還原)"
]
VIDEO_QUALITIES = [
    "最高畫質 (最佳/推薦)",
    "2160p (4K Ultra HD)",
    "1440p (2K Quad HD)",
    "1080p (Full HD)",
    "720p (HD)",
    "480p (標清)",
    "360p (節省空間)"
]

def extract_format_code(display_str: str) -> str:
    """從格式顯示名稱提取純副檔名 (如 'mp3', 'wav', 'mp4')"""
    s = display_str.split()[0].lower().strip()
    for f in ('mp3', 'm4a', 'wav', 'flac', 'aac', 'ogg', 'opus', 'mp4', 'mkv', 'webm', 'mov', 'avi'):
        if s.startswith(f):
            return f
    return "mp3"


def load_app_config() -> dict:
    """載入應用程式使用者設定"""
    default_config = {
        "language": "zh_TW",
        "auto_check_update": True,
        "install_date": None,
        "preferred_format": "mp3",
    }
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                default_config.update(data)
    except Exception:
        pass
    i18n.set_current_language(default_config.get("language", "zh_TW"))
    return default_config


def save_app_config(cfg: dict):
    """保存應用程式使用者設定"""
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def get_install_date_str() -> str:
    """獲取軟體安裝日期（若未記錄則自動讀取執行檔建立時間並持久化儲存）"""
    cfg = load_app_config()
    if cfg.get("install_date"):
        return cfg["install_date"]

    target_path = sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__)
    try:
        ctime = os.path.getctime(target_path)
        dt = datetime.fromtimestamp(ctime)
        date_str = dt.strftime("%Y年%m月%d日 %H:%M")
    except Exception:
        date_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    cfg["install_date"] = date_str
    save_app_config(cfg)
    return date_str


def check_for_updates(parent=None, silent=False):
    """在背景執行緒中檢查 GitHub 最新版本"""
    def _worker():
        try:
            req = urllib.request.Request(
                GITHUB_RELEASES_API,
                headers={"User-Agent": "StreamForge-Desktop-App"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    raw_tag = data.get("tag_name", "").lstrip("v")
                    html_url = data.get("html_url", GITHUB_RELEASES_URL)

                    def parse_v(v_str):
                        parts = []
                        for p in v_str.split("."):
                            try:
                                parts.append(int(p))
                            except ValueError:
                                parts.append(0)
                        return parts

                    latest_v = parse_v(raw_tag) if raw_tag else []
                    curr_v = parse_v(APP_VERSION)

                    # 尋找直接下載的安裝檔網址 (.exe)
                    direct_exe_url = None
                    for asset in data.get("assets", []):
                        if asset.get("name", "").endswith(".exe"):
                            direct_exe_url = asset.get("browser_download_url")
                            break

                    if latest_v and latest_v > curr_v:
                        if parent and parent.winfo_exists():
                            parent.after(0, lambda: _prompt_update(parent, raw_tag, html_url, direct_exe_url))
                        return
                    else:
                        if not silent and parent and parent.winfo_exists():
                            parent.after(0, lambda: messagebox.showinfo(
                                "版本檢查",
                                f"🎉 目前已是最新版本 (v{APP_VERSION})！"
                            ))
                        return
        except Exception:
            if not silent and parent and parent.winfo_exists():
                parent.after(0, lambda: messagebox.showinfo(
                    "檢查更新提示",
                    f"目前使用版本：v{APP_VERSION}\n若要獲取最新發布安裝檔或原始碼，請前往官方 GitHub Releases 頁面。"
                ))

    t = threading.Thread(target=_worker, daemon=True)
    t.start()


class UpdateDownloadDialog(ctk.CTkToplevel):
    """自動下載新版安裝檔並執行升級的進度視窗"""
    def __init__(self, parent, new_version: str, download_url: str):
        super().__init__(parent)
        apply_window_icon(self)
        self.title("🚀 StreamForge - 正在自動下載更新")
        self.geometry("460x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.new_version = new_version
        self.download_url = download_url
        self.cancelled = False

        lbl_title = ctk.CTkLabel(
            self,
            text=f"正在下載 StreamForge v{new_version} 更新安裝檔...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#38bdf8"
        )
        lbl_title.pack(padx=20, pady=(20, 10))

        self.lbl_status = ctk.CTkLabel(
            self,
            text="連線中...",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.lbl_status.pack(padx=20, pady=(0, 10))

        self.progress_bar = ctk.CTkProgressBar(self, width=380, height=14)
        self.progress_bar.pack(padx=20, pady=(0, 15))
        self.progress_bar.set(0.0)

        self.btn_cancel = ctk.CTkButton(
            self,
            text="取消下載",
            width=100,
            height=32,
            fg_color="#334155",
            hover_color="#475569",
            command=self._cancel
        )
        self.btn_cancel.pack(pady=(0, 15))

        threading.Thread(target=self._start_download, daemon=True).start()

    def _cancel(self):
        self.cancelled = True
        self.destroy()

    def _start_download(self):
        temp_dir = os.environ.get("TEMP", os.path.expanduser("~"))
        target_path = os.path.join(temp_dir, f"StreamForge-Setup-v{self.new_version}.exe")
        try:
            req = urllib.request.Request(
                self.download_url,
                headers={"User-Agent": "StreamForge-Desktop-App"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                total_size = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                chunk_size = 64 * 1024

                with open(target_path, "wb") as f:
                    while True:
                        if self.cancelled:
                            return
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            pct = downloaded / total_size
                            self.after(0, lambda p=pct, d=downloaded, t=total_size: self._update_ui(p, d, t))

            if not self.cancelled:
                self.after(0, lambda: self._on_download_complete(target_path))
        except Exception as e:
            if not self.cancelled:
                self.after(0, lambda: messagebox.showerror("更新失敗", f"下載更新檔時發生錯誤：\n{e}\n\n請手動前往 GitHub 頁面下載。"))
                self.after(0, self.destroy)

    def _update_ui(self, pct, downloaded, total):
        if not self.winfo_exists():
            return
        self.progress_bar.set(pct)
        mb_down = downloaded / (1024 * 1024)
        mb_tot = total / (1024 * 1024)
        self.lbl_status.configure(text=f"已下載: {mb_down:.1f} MB / {mb_tot:.1f} MB ({pct*100:.0f}%)")

    def _on_download_complete(self, target_path):
        if not self.winfo_exists():
            return
        self.destroy()
        res = messagebox.askyesno(
            "下載完成",
            f"🎉 StreamForge v{self.new_version} 安裝檔已下載完畢！\n\n是否立即啟動安裝程式進行覆蓋更新？\n(程式將自動關閉以進行更新)"
        )
        if res:
            try:
                subprocess.Popen([target_path])
                os._exit(0)
            except Exception as e:
                messagebox.showerror("啟動失敗", f"無法啟動安裝程式：{e}")


def _prompt_update(parent, new_version, release_url, direct_exe_url=None):
    if direct_exe_url:
        res = messagebox.askyesno(
            "發現新版本",
            f"🚀 發現 StreamForge 新版本 v{new_version}！\n\n目前版本：v{APP_VERSION}\n\n點選【是 (Yes)】：立即自動下載更新並安裝\n點選【否 (No)】：前往 GitHub 網頁查看更新日誌",
            icon="question"
        )
        if res:
            UpdateDownloadDialog(parent, new_version, direct_exe_url)
        else:
            webbrowser.open(release_url)
    else:
        res = messagebox.askyesno(
            "發現新版本",
            f"🚀 發現 StreamForge 新版本 v{new_version}！\n\n目前版本：v{APP_VERSION}\n請問是否前往 GitHub Releases 頁面下載新版本？"
        )
        if res:
            webbrowser.open(release_url)



class FormatFactoryDialog(ctk.CTkToplevel):
    """
    StreamForge 格式工廠 · 本地媒體轉檔視窗
    允許選取本機現有影音檔案，使用內建高效 FFmpeg 批次轉檔為各種音訊或視訊格式
    """
    def __init__(self, parent, default_out_dir: str = "", log_callback: Optional[Callable[[str], None]] = None):
        super().__init__(parent)
        apply_window_icon(self)
        self.title("🎛️ StreamForge 格式工廠 · 本地媒體轉檔")
        self.geometry("680x580")
        self.minsize(580, 480)
        self.transient(parent)
        self.grab_set()

        self.parent = parent
        self.log_callback = log_callback
        self.files_to_convert = []
        self.default_out_dir = default_out_dir or os.path.join(get_windows_user_downloads_dir(), "StreamForge")

        # 頂部標題
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=(16, 8))

        lbl_t = ctk.CTkLabel(
            top_frame,
            text="🎛️ 本地多媒體格式工廠 (FFmpeg 核心加速)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#38bdf8"
        )
        lbl_t.pack(anchor="w")

        lbl_sub = ctk.CTkLabel(
            top_frame,
            text="直接在本機批次轉換音訊或影片格式，支援 MP3, WAV, FLAC, M4A, AAC, OGG, OPUS, MP4, MKV, WEBM, MOV, AVI 等",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        lbl_sub.pack(anchor="w", pady=(2, 0))

        # 1. 檔案選取區塊
        file_box = ctk.CTkFrame(self, corner_radius=8)
        file_box.pack(fill="both", expand=True, padx=20, pady=8)

        file_toolbar = ctk.CTkFrame(file_box, fg_color="transparent")
        file_toolbar.pack(fill="x", padx=12, pady=(10, 6))

        btn_add = ctk.CTkButton(
            file_toolbar,
            text="📁 選取檔案 (可多選)",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._choose_files,
            width=140
        )
        btn_add.pack(side="left", padx=(0, 8))

        btn_clear = ctk.CTkButton(
            file_toolbar,
            text="🗑️ 清空清單",
            font=ctk.CTkFont(size=12),
            fg_color="#475569",
            hover_color="#334155",
            command=self._clear_files,
            width=90
        )
        btn_clear.pack(side="left")

        self.lbl_file_count = ctk.CTkLabel(
            file_toolbar,
            text="已選擇 0 個檔案",
            font=ctk.CTkFont(size=12),
            text_color="#cbd5e1"
        )
        self.lbl_file_count.pack(side="right")

        self.scroll_files = ctk.CTkScrollableFrame(file_box, height=140)
        self.scroll_files.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        # 2. 轉檔目標設定區塊
        opts_frame = ctk.CTkFrame(self, corner_radius=8)
        opts_frame.pack(fill="x", padx=20, pady=6)

        r1 = ctk.CTkFrame(opts_frame, fg_color="transparent")
        r1.pack(fill="x", padx=12, pady=(10, 6))

        ctk.CTkLabel(r1, text="目標類型：", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(0, 4))
        self.seg_conv_type = ctk.CTkSegmentedButton(
            r1,
            values=["🎵 音訊", "🎬 視訊"],
            command=self._on_type_changed,
            width=140
        )
        self.seg_conv_type.set("🎵 音訊")
        self.seg_conv_type.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(r1, text="目標格式：", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(0, 4))
        self.opt_conv_format = ctk.CTkOptionMenu(
            r1,
            values=AUDIO_FORMAT_OPTIONS,
            command=self._on_format_changed,
            width=150
        )
        self.opt_conv_format.set(AUDIO_FORMAT_OPTIONS[0])
        self.opt_conv_format.pack(side="left", padx=(0, 14))

        ctk.CTkLabel(r1, text="輸出品質：", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(0, 4))
        self.opt_conv_quality = ctk.CTkOptionMenu(
            r1,
            values=AUDIO_QUALITIES_LOSSY,
            width=150
        )
        self.opt_conv_quality.set(AUDIO_QUALITIES_LOSSY[0])
        self.opt_conv_quality.pack(side="left")

        # 儲存目錄
        r2 = ctk.CTkFrame(opts_frame, fg_color="transparent")
        r2.pack(fill="x", padx=12, pady=(4, 10))

        ctk.CTkLabel(r2, text="儲存目錄：", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(0, 4))
        self.entry_out_dir = ctk.CTkEntry(r2, height=30)
        self.entry_out_dir.insert(0, self.default_out_dir)
        self.entry_out_dir.pack(side="left", fill="x", expand=True, padx=(0, 8))

        btn_browse = ctk.CTkButton(
            r2,
            text="瀏覽...",
            width=70,
            height=30,
            command=self._browse_dir
        )
        btn_browse.pack(side="left")

        # 3. 進度與執行列
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=(6, 16))

        self.lbl_conv_status = ctk.CTkLabel(
            action_frame,
            text="就緒，請選取檔案後點擊「開始批次轉檔」",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.lbl_conv_status.pack(anchor="w", pady=(0, 4))

        self.progress_bar = ctk.CTkProgressBar(action_frame, height=12)
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0.0)

        btn_row = ctk.CTkFrame(action_frame, fg_color="transparent")
        btn_row.pack(fill="x")

        self.btn_start = ctk.CTkButton(
            btn_row,
            text="🚀 開始批次轉檔",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            height=34,
            command=self._start_convert
        )
        self.btn_start.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_open_out = ctk.CTkButton(
            btn_row,
            text="📂 開啟輸出目錄",
            height=34,
            fg_color="#334155",
            hover_color="#475569",
            command=self._open_output_dir
        )
        self.btn_open_out.pack(side="right")

        self._render_file_list()

    def _choose_files(self):
        filetypes = [
            ("所有支援媒體格式", "*.mp3;*.wav;*.flac;*.m4a;*.aac;*.ogg;*.opus;*.mp4;*.mkv;*.webm;*.mov;*.avi;*.wma;*.wmv;*.flv;*.ts;*.m4v"),
            ("音訊檔案 (*.mp3;*.wav;*.flac;*.m4a...)", "*.mp3;*.wav;*.flac;*.m4a;*.aac;*.ogg;*.opus;*.wma"),
            ("視訊檔案 (*.mp4;*.mkv;*.webm;*.mov...)", "*.mp4;*.mkv;*.webm;*.mov;*.avi;*.wmv;*.flv;*.ts;*.m4v"),
            ("所有檔案 (*.*)", "*.*")
        ]
        chosen = filedialog.askopenfilenames(title="選取要轉檔的檔案", filetypes=filetypes)
        if chosen:
            for p in chosen:
                if p not in self.files_to_convert:
                    self.files_to_convert.append(p)
            self._render_file_list()

    def _clear_files(self):
        self.files_to_convert.clear()
        self._render_file_list()

    def _render_file_list(self):
        for w in self.scroll_files.winfo_children():
            w.destroy()

        self.lbl_file_count.configure(text=f"已選擇 {len(self.files_to_convert)} 個檔案")

        if not self.files_to_convert:
            lbl_empty = ctk.CTkLabel(
                self.scroll_files,
                text="尚未選取任何檔案，請點擊上方「選取檔案」",
                text_color="#64748b"
            )
            lbl_empty.pack(pady=20)
            return

        for idx, fpath in enumerate(self.files_to_convert):
            row = ctk.CTkFrame(self.scroll_files, fg_color="#1e293b", corner_radius=6)
            row.pack(fill="x", pady=2, padx=2)

            fname = os.path.basename(fpath)
            try:
                fsize = os.path.getsize(fpath)
                size_str = f"{fsize / (1024 * 1024):.1f} MB"
            except Exception:
                size_str = "未知大小"

            lbl_name = ctk.CTkLabel(
                row,
                text=f"{idx + 1}. {fname} ({size_str})",
                anchor="w",
                font=ctk.CTkFont(size=12)
            )
            lbl_name.pack(side="left", padx=8, fill="x", expand=True)

            btn_del = ctk.CTkButton(
                row,
                text="✕",
                width=24,
                height=24,
                fg_color="#ef4444",
                hover_color="#dc2626",
                command=lambda p=fpath: self._remove_single_file(p)
            )
            btn_del.pack(side="right", padx=6)

    def _remove_single_file(self, path):
        if path in self.files_to_convert:
            self.files_to_convert.remove(path)
            self._render_file_list()

    def _browse_dir(self):
        p = filedialog.askdirectory(title="選擇轉檔儲存目錄", initialdir=self.entry_out_dir.get())
        if p:
            self.entry_out_dir.delete(0, tk.END)
            self.entry_out_dir.insert(0, p)

    def _open_output_dir(self):
        d = self.entry_out_dir.get().strip()
        if os.path.exists(d):
            try:
                os.startfile(d)
            except Exception as ex:
                messagebox.showerror("錯誤", f"無法開啟目錄: {ex}")
        else:
            messagebox.showinfo("提示", "輸出目錄目前尚不存在！")

    def _on_type_changed(self, value):
        if "視訊" in value:
            self.opt_conv_format.configure(values=VIDEO_FORMAT_OPTIONS)
            self.opt_conv_format.set(VIDEO_FORMAT_OPTIONS[0])
            self._on_format_changed(VIDEO_FORMAT_OPTIONS[0])
        else:
            self.opt_conv_format.configure(values=AUDIO_FORMAT_OPTIONS)
            self.opt_conv_format.set(AUDIO_FORMAT_OPTIONS[0])
            self._on_format_changed(AUDIO_FORMAT_OPTIONS[0])

    def _on_format_changed(self, value):
        fmt = extract_format_code(value)
        if fmt in ('wav', 'flac'):
            self.opt_conv_quality.configure(values=AUDIO_QUALITIES_LOSSLESS)
            self.opt_conv_quality.set(AUDIO_QUALITIES_LOSSLESS[0])
        elif fmt in ('mp3', 'm4a', 'aac', 'ogg', 'opus'):
            self.opt_conv_quality.configure(values=AUDIO_QUALITIES_LOSSY)
            self.opt_conv_quality.set(AUDIO_QUALITIES_LOSSY[0])
        else:
            self.opt_conv_quality.configure(values=VIDEO_QUALITIES)
            self.opt_conv_quality.set(VIDEO_QUALITIES[0])

    def _start_convert(self):
        if not self.files_to_convert:
            messagebox.showwarning("提示", "請先選取要轉檔的檔案！")
            return

        out_dir = self.entry_out_dir.get().strip()
        if not out_dir:
            messagebox.showwarning("提示", "請設定輸出儲存目錄！")
            return

        os.makedirs(out_dir, exist_ok=True)
        target_fmt = extract_format_code(self.opt_conv_format.get())
        q_raw = self.opt_conv_quality.get()
        quality = q_raw.split()[0] if q_raw else "320"

        self.btn_start.configure(state="disabled", text="⏳ 轉檔進行中...")
        self.progress_bar.set(0.0)

        def _worker():
            total = len(self.files_to_convert)
            success = 0
            fail = 0

            for i, src in enumerate(self.files_to_convert, 1):
                fname = os.path.basename(src)
                stem, _ = os.path.splitext(fname)
                out_path = os.path.join(out_dir, f"{stem}.{target_fmt}")

                self.after(0, lambda idx=i, t=total, n=fname: self.lbl_conv_status.configure(
                    text=f"🔄 [{idx}/{t}] 正在轉檔: {n} -> {target_fmt.upper()}"
                ))

                try:
                    downloader.convert_local_media(
                        input_path=src,
                        output_path=out_path,
                        target_format=target_fmt,
                        quality=quality,
                        log_callback=self.log_callback
                    )
                    success += 1
                except Exception as ex:
                    fail += 1
                    if self.log_callback:
                        self.log_callback(f"❌ [轉檔失敗] {fname}: {ex}")

                pct = i / total
                self.after(0, lambda p=pct: self.progress_bar.set(p))

            def _finish():
                self.btn_start.configure(state="normal", text="🚀 開始批次轉檔")
                self.lbl_conv_status.configure(text=f"🎉 批次轉檔完成！成功: {success}，失敗: {fail}")
                messagebox.showinfo("格式工廠轉檔完成", f"🎉 已完成批次轉檔！\n\n成功：{success} 個檔案\n失敗：{fail} 個檔案\n\n輸出目錄：{out_dir}")

            self.after(0, _finish)

        threading.Thread(target=_worker, daemon=True).start()


class DuplicateDialog(ctk.CTkToplevel):
    """發現重複檔案時的選擇互動視窗"""
    def __init__(self, parent, song_title: str, existing_filename: str):
        super().__init__(parent)
        apply_window_icon(self)
        self.title("⚠️ 發現重複檔案 - 選擇處理方式")
        self.geometry("540x350")
        self.resizable(False, False)

        self.action = "skip"  # 'overwrite', 'suffix', 'skip'
        self.apply_all = False

        self.transient(parent)
        self.grab_set()

        lbl_icon = ctk.CTkLabel(
            self,
            text="⚠️ 發現重複檔案！",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#f59e0b"
        )
        lbl_icon.pack(padx=20, pady=(15, 6))

        info_box = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=8)
        info_box.pack(padx=20, pady=6, fill="x")

        display_title = song_title if len(song_title) <= 50 else song_title[:47] + "..."
        lbl_song = ctk.CTkLabel(
            info_box,
            text=f"準備下載：{display_title}",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w",
            text_color="#f8fafc"
        )
        lbl_song.pack(padx=12, pady=(8, 2), fill="x")

        lbl_exist = ctk.CTkLabel(
            info_box,
            text=f"現有檔案：{existing_filename}",
            font=ctk.CTkFont(size=12),
            anchor="w",
            text_color="#94a3b8"
        )
        lbl_exist.pack(padx=12, pady=(2, 8), fill="x")

        lbl_prompt = ctk.CTkLabel(
            self,
            text="目標資料夾中已存在同名或相同歌曲，請問您希望如何處理？",
            font=ctk.CTkFont(size=12)
        )
        lbl_prompt.pack(padx=20, pady=4)

        # 套用到全部
        self.chk_all = ctk.CTkCheckBox(
            self,
            text="☑️ 套用到後續所有重複檔案（本次任務不再詢問）",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.chk_all.pack(padx=20, pady=8)

        # 按鈕群組
        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(padx=20, pady=(8, 15), fill="x")
        btn_box.grid_columnconfigure((0, 1, 2), weight=1)

        btn_ovr = ctk.CTkButton(
            btn_box,
            text="🔁 覆蓋檔案",
            fg_color="#f59e0b",
            hover_color="#d97706",
            height=38,
            command=lambda: self._choose("overwrite")
        )
        btn_ovr.grid(row=0, column=0, padx=4, sticky="ew")

        btn_suf = ctk.CTkButton(
            btn_box,
            text="➕ 加上 (1) 後綴",
            fg_color="#0284c7",
            hover_color="#0369a1",
            height=38,
            command=lambda: self._choose("suffix")
        )
        btn_suf.grid(row=0, column=1, padx=4, sticky="ew")

        btn_skp = ctk.CTkButton(
            btn_box,
            text="⏭️ 略過此首",
            fg_color="#64748b",
            hover_color="#475569",
            height=38,
            command=lambda: self._choose("skip")
        )
        btn_skp.grid(row=0, column=2, padx=4, sticky="ew")

    def _choose(self, choice: str):
        self.action = choice
        self.apply_all = bool(self.chk_all.get())
        self.destroy()


class FailureReportDialog(ctk.CTkToplevel):
    """下載失敗項目清單與重試對話框"""
    def __init__(self, parent, failed_items: list, retry_callback):
        super().__init__(parent)
        apply_window_icon(self)
        self.title("❌ 下載失敗項目報告與重試")
        self.geometry("680x480")
        self.minsize(560, 380)
        self.transient(parent)
        self.grab_set()

        lbl_title = ctk.CTkLabel(
            self,
            text=f"⚠️ 下載完成，但有 {len(failed_items)} 個項目發生錯誤！",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ef4444"
        )
        lbl_title.pack(padx=15, pady=(15, 4))

        lbl_desc = ctk.CTkLabel(
            self,
            text="以下列出所有下載失敗的曲目與原因，您可以點擊下方按鈕直接一鍵重試：",
            font=ctk.CTkFont(size=12),
            text_color="#cbd5e1"
        )
        lbl_desc.pack(padx=15, pady=(0, 8))

        scroll = ctk.CTkScrollableFrame(self, height=280)
        scroll.pack(padx=15, pady=6, fill="both", expand=True)

        for i, item in enumerate(failed_items, 1):
            f_frame = ctk.CTkFrame(scroll, fg_color="#1e293b", corner_radius=6)
            f_frame.pack(fill="x", padx=4, pady=4)

            t_lbl = ctk.CTkLabel(
                f_frame,
                text=f"{i}. {item['title']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
                text_color="#f8fafc"
            )
            t_lbl.pack(padx=10, pady=(6, 2), anchor="w", fill="x")

            err_text = item.get('error', '未知錯誤')
            friendly_hint = ""
            if "Private video" in err_text:
                friendly_hint = "💡 [診斷：該影片為私人影片或已被發布者刪除]"
            elif "Sign in to confirm" in err_text or "bot" in err_text.lower():
                friendly_hint = "💡 [診斷：伺服器觸發機器人驗證機制]"
            elif "HTTP Error 403" in err_text:
                friendly_hint = "💡 [診斷：HTTP 403 存取受限，重試或稍後再試通常可解決]"
            elif "timed out" in err_text.lower():
                friendly_hint = "💡 [診斷：網路連線逾時]"

            e_lbl = ctk.CTkLabel(
                f_frame,
                text=f"錯誤原因：{err_text[:140]}... {friendly_hint}",
                font=ctk.CTkFont(size=11),
                anchor="w",
                text_color="#f87171",
                justify="left",
                wraplength=600
            )
            e_lbl.pack(padx=10, pady=(0, 6), anchor="w", fill="x")

        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(padx=15, pady=(8, 15), fill="x")

        btn_retry = ctk.CTkButton(
            btn_box,
            text=f"🔄 立即重試這 {len(failed_items)} 個失敗項目",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            height=38,
            command=lambda: [self.destroy(), retry_callback()]
        )
        btn_retry.pack(side="left", padx=(0, 8), expand=True, fill="x")

        btn_close = ctk.CTkButton(
            btn_box,
            text="關閉",
            width=90,
            height=38,
            fg_color="#475569",
            hover_color="#64748b",
            command=self.destroy
        )
        btn_close.pack(side="right")


class AboutDialog(ctk.CTkToplevel):
    """關於 StreamForge、版權宣告、授權條款與自動更新對話框 (支援多國語言)"""
    def __init__(self, parent):
        super().__init__(parent)
        apply_window_icon(self)
        self.title(i18n.t("about_title"))
        self.geometry("640x670")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.parent = parent
        self.cfg = load_app_config()
        self.install_date_str = get_install_date_str()

        # 頂部 Logo 品牌圖示
        logo_file = get_asset_path("logo.png")
        if os.path.exists(logo_file):
            try:
                pil_logo = Image.open(logo_file)
                self.logo_ctk_img = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(72, 72))
                lbl_icon = ctk.CTkLabel(self, text="", image=self.logo_ctk_img)
                lbl_icon.pack(padx=20, pady=(12, 2))
            except Exception:
                pass

        # 頂部標題
        lbl_logo = ctk.CTkLabel(
            self,
            text="⚡ StreamForge",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#38bdf8"
        )
        lbl_logo.pack(padx=20, pady=(2, 2))

        lbl_version = ctk.CTkLabel(
            self,
            text=f"Version {APP_VERSION} (Windows 64-bit) · {i18n.t('product_name_lbl')}",
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        lbl_version.pack(padx=20, pady=(0, 6))

        # 頁籤容器
        tabview = ctk.CTkTabview(self, width=600, height=430)
        tabview.pack(padx=20, pady=(0, 10), fill="both", expand=True)

        tab_about = tabview.add(i18n.t("tab_about"))
        tab_disclaimer = tabview.add(i18n.t("tab_disclaimer"))
        tab_license = tabview.add(i18n.t("tab_license"))

        # ------------------ Tab 1: 關於我們 ------------------
        info_card = ctk.CTkFrame(tab_about, fg_color="#1e293b", corner_radius=8)
        info_card.pack(padx=10, pady=8, fill="x")

        # 語言選擇下拉選單
        row_lang = ctk.CTkFrame(info_card, fg_color="transparent")
        row_lang.pack(fill="x", padx=12, pady=(8, 4))
        ctk.CTkLabel(row_lang, text=i18n.t("lang_selector_label"), font=ctk.CTkFont(size=12, weight="bold"), width=160, anchor="w", text_color="#38bdf8").pack(side="left")
        
        curr_lang_name = i18n.LANGUAGES.get(i18n.get_current_language(), "繁體中文")
        self.opt_dialog_lang = ctk.CTkOptionMenu(
            row_lang,
            values=list(i18n.LANGUAGES.values()),
            width=130,
            height=28,
            command=self._on_change_dialog_lang
        )
        self.opt_dialog_lang.set(curr_lang_name)
        self.opt_dialog_lang.pack(side="left")

        items = [
            (i18n.t("product_name_lbl"), "StreamForge"),
            (i18n.t("install_date_lbl"), self.install_date_str),
            (i18n.t("dev_team_lbl"), "The StreamForge Team & Contributors"),
            (i18n.t("license_lbl"), "MIT License"),
            (i18n.t("copyright_lbl"), "© 2026 The StreamForge Team. All Rights Reserved."),
            (i18n.t("project_home_lbl"), f"https://github.com/{GITHUB_REPO}")
        ]

        for label, val in items:
            row_f = ctk.CTkFrame(info_card, fg_color="transparent")
            row_f.pack(fill="x", padx=12, pady=3)
            ctk.CTkLabel(row_f, text=label, font=ctk.CTkFont(size=12, weight="bold"), width=160, anchor="w", text_color="#38bdf8").pack(side="left")
            ctk.CTkLabel(row_f, text=val, font=ctk.CTkFont(size=12), anchor="w", text_color="#f1f5f9").pack(side="left", fill="x", expand=True)

        # 更新設定與手動檢查卡片
        update_card = ctk.CTkFrame(tab_about, fg_color="#0f172a", corner_radius=8)
        update_card.pack(padx=10, pady=8, fill="x")

        self.var_autocheck = tk.BooleanVar(value=self.cfg.get("auto_check_update", True))
        chk_autoupdate = ctk.CTkCheckBox(
            update_card,
            text=i18n.t("chk_autoupdate"),
            variable=self.var_autocheck,
            font=ctk.CTkFont(size=12),
            command=self._on_toggle_autocheck
        )
        chk_autoupdate.pack(padx=12, pady=(10, 8), anchor="w")

        btn_row = ctk.CTkFrame(update_card, fg_color="transparent")
        btn_row.pack(fill="x", padx=12, pady=(0, 10))

        btn_check_now = ctk.CTkButton(
            btn_row,
            text=i18n.t("btn_check_now"),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=130,
            height=32,
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=lambda: check_for_updates(parent=self, silent=False)
        )
        btn_check_now.pack(side="left", padx=(0, 8))

        btn_open_repo = ctk.CTkButton(
            btn_row,
            text=i18n.t("btn_open_repo"),
            font=ctk.CTkFont(size=12),
            width=140,
            height=32,
            fg_color="#334155",
            hover_color="#475569",
            command=lambda: webbrowser.open(GITHUB_RELEASES_URL)
        )
        btn_open_repo.pack(side="left")

        # ------------------ Tab 2: 法律免責聲明 ------------------
        disclaimer_text = (
            "【法律免責聲明 (Legal Disclaimer)】\n\n"
            "1. 【開源目的與合理使用】\n"
            "   本工具為開放原始碼專案，開發目的僅供個人學習、研究、合理使用 (Fair Use)\n"
            "   以及備份個人已取得授權或合法擁有之影音媒體內容。\n\n"
            "2. 【無伺服器與無代管保證】\n"
            "   StreamForge 為純客戶端本地工具，不提供、不儲存、亦不分發或代管任何\n"
            "   受著作權保護之媒體內容與資料庫。\n\n"
            "3. 【智慧財產權與商標歸屬】\n"
            "   所有透過本工具下載之影音內容，其著作權、商標權及其他各項智慧財產權，\n"
            "   均完整歸屬於原創作者、版權持有人及各來源串流平台所有。\n\n"
            "4. 【使用者之完全法律責任】\n"
            "   使用者使用本軟體下載或轉檔時，應嚴格遵守所在國家/地區之智慧財產權法規\n"
            "   及各串流平台之服務使用條款。任何因未經授權之商業利用、重製或二次散佈行為\n"
            "   所衍生之一切法律糾紛或民刑事責任，概由使用者本人完全承擔，\n"
            "   開發團隊不承擔任何直接、間接或連帶賠償責任。"
        )
        txt_disclaimer = ctk.CTkTextbox(tab_disclaimer, font=ctk.CTkFont(family="Consolas", size=11), text_color="#e2e8f0")
        txt_disclaimer.pack(fill="both", expand=True, padx=6, pady=6)
        txt_disclaimer.insert("1.0", disclaimer_text)
        txt_disclaimer.configure(state="disabled")

        # ------------------ Tab 3: MIT License ------------------
        license_text = (
            "MIT License\n\n"
            "Copyright (c) 2026 The StreamForge Team & Contributors\n\n"
            "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
            "of this software and associated documentation files (the \"Software\"), to deal\n"
            "in the Software without restriction, including without limitation the rights\n"
            "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
            "copies of the Software, and to permit persons to whom the Software is\n"
            "furnished to do so, subject to the following conditions:\n\n"
            "The above copyright notice and this permission notice shall be included in all\n"
            "copies or substantial portions of the Software.\n\n"
            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
            "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
            "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
            "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
            "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
            "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n"
            "SOFTWARE."
        )
        txt_license = ctk.CTkTextbox(tab_license, font=ctk.CTkFont(family="Consolas", size=11), text_color="#cbd5e1")
        txt_license.pack(fill="both", expand=True, padx=6, pady=6)
        txt_license.insert("1.0", license_text)
        txt_license.configure(state="disabled")

        # 底部按鈕區
        btn_box = ctk.CTkFrame(self, fg_color="transparent")
        btn_box.pack(padx=20, pady=(0, 14), fill="x")

        full_copy_text = f"StreamForge v{APP_VERSION}\n安裝日期: {self.install_date_str}\n\n{disclaimer_text}\n\n{license_text}"

        btn_copy = ctk.CTkButton(
            btn_box,
            text=i18n.t("btn_copy_disclaimer"),
            font=ctk.CTkFont(size=12),
            width=160,
            height=34,
            fg_color="#334155",
            hover_color="#475569",
            command=lambda: self._copy_info(parent, full_copy_text)
        )
        btn_copy.pack(side="left")

        btn_close = ctk.CTkButton(
            btn_box,
            text=i18n.t("btn_close"),
            font=ctk.CTkFont(size=12, weight="bold"),
            width=90,
            height=34,
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self.destroy
        )
        btn_close.pack(side="right")

    def _on_change_dialog_lang(self, lang_name):
        if self.parent and hasattr(self.parent, '_on_change_language'):
            self.parent._on_change_language(lang_name)
        self.destroy()
        if self.parent and hasattr(self.parent, 'show_about_dialog'):
            self.parent.show_about_dialog()

    def _on_toggle_autocheck(self):
        val = self.var_autocheck.get()
        self.cfg["auto_check_update"] = val
        save_app_config(self.cfg)

    def _copy_info(self, parent, text):
        try:
            parent.clipboard_clear()
            parent.clipboard_append(text)
            messagebox.showinfo("提示", "已將完整版權宣告與法律免責聲明複製至剪貼簿！")
        except Exception:
            pass


class MediaDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StreamForge v1.0.0 · 串流影音工坊 (多格式下載 / 本地轉檔 · 命令終端版)")
        self.geometry("1060 x 870")
        self.minsize(920, 720)
        apply_window_icon(self)

        # 讀取使用者設定檔並在啟用時進行自動更新檢查
        self.app_config = load_app_config()
        saved_lang = self.app_config.get("language", "zh_TW")
        i18n.set_current_language(saved_lang)

        # 預設儲存目錄（動態精確偵測 Windows 使用者的真實下載目錄，支援轉移至 D:、E: 槽或自訂路徑之設定）
        real_downloads = get_windows_user_downloads_dir()
        user_downloads = os.path.join(real_downloads, "StreamForge")
        configured_dir = self.app_config.get("download_dir", "")
        if configured_dir and os.path.isdir(configured_dir):
            self.default_download_dir = configured_dir
        else:
            self.default_download_dir = user_downloads

        try:
            os.makedirs(self.default_download_dir, exist_ok=True)
        except Exception:
            # 萬一受限，回退至使用者家目錄
            self.default_download_dir = os.path.join(os.path.expanduser("~"), "StreamForge")
            try:
                os.makedirs(self.default_download_dir, exist_ok=True)
            except Exception:
                self.default_download_dir = os.path.expanduser("~")

        self.songs = []  # 儲存清單項目
        self.song_widgets = []  # 儲存 UI 元件
        self.is_running = False
        self.is_paused = False
        self.cancel_requested = False
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.next_number = 1  # 接續編號起點
        self.duplicate_action_all = None  # 批次內套用全部的重複處理選項
        self.failed_items = []  # 失敗歌曲資訊
        self.console_visible = True
        self.cmd_history = []
        self.cmd_history_idx = -1
        self._log_queue = []
        self._log_lock = threading.Lock()
        self._log_flushing = False
        self.duplicate_lock = threading.Lock()
        self.btn_download = None
        self.btn_pause = None
        self.btn_cancel = None
        self.lbl_threads = None
        self.opt_threads = None
        self.lbl_quality = None
        self.opt_quality = None
        self.chk_thumb = None

        self._build_ui()
        self._detect_usb_drives()
        self.log("🚀 StreamForge v1.0.0 就緒！© 2026 The StreamForge Team. All Rights Reserved.")
        self.log("💡 可在下方輸入指令（輸入 'help' 查看所有可用指令），支援 ↑/↓ 鍵歷史紀錄。")

        if self.app_config.get("auto_check_update", True):
            self.after(1500, lambda: check_for_updates(parent=self, silent=True))

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # ================= 1. 頂部標題列 =================
        header_frame = ctk.CTkFrame(self, corner_radius=10)
        header_frame.grid(row=0, column=0, padx=15, pady=(12, 6), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        # 標題與版權按鈕列
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.grid(row=0, column=0, padx=15, pady=(8, 2), sticky="ew")
        title_box.grid_columnconfigure(0, weight=1)

        self.title_lbl = ctk.CTkLabel(
            title_box,
            text=i18n.t("app_title"),
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#38bdf8"
        )
        self.title_lbl.pack(side="left")

        curr_lang = self.app_config.get("language", "zh_TW")
        curr_lang_name = i18n.LANGUAGES.get(curr_lang, "繁體中文")

        self.opt_lang = ctk.CTkOptionMenu(
            title_box,
            values=list(i18n.LANGUAGES.values()),
            width=110,
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#1e293b",
            button_color="#334155",
            button_hover_color="#475569",
            command=self._on_change_language
        )
        self.opt_lang.set(curr_lang_name)
        self.opt_lang.pack(side="right", padx=(8, 0))

        self.btn_about = ctk.CTkButton(
            title_box,
            text=i18n.t("btn_about"),
            font=ctk.CTkFont(size=11, weight="bold"),
            width=120,
            height=26,
            fg_color="#1e293b",
            hover_color="#334155",
            border_width=1,
            border_color="#475569",
            command=self.show_about_dialog
        )
        self.btn_about.pack(side="right")

        self.sub_lbl = ctk.CTkLabel(
            header_frame,
            text=i18n.t("app_subtitle"),
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8"
        )
        self.sub_lbl.grid(row=1, column=0, padx=15, pady=(0, 8), sticky="w")

        # ================= 2. 單條輸入與加入區 =================
        add_frame = ctk.CTkFrame(self, corner_radius=10)
        add_frame.grid(row=1, column=0, padx=15, pady=4, sticky="ew")
        add_frame.grid_columnconfigure(0, weight=1)

        self.input_title = ctk.CTkLabel(
            add_frame,
            text=i18n.t("sec_add_song"),
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.input_title.grid(row=0, column=0, columnspan=4, padx=14, pady=(8, 4), sticky="w")

        # 單行輸入框
        self.entry_url = ctk.CTkEntry(
            add_frame,
            placeholder_text=i18n.t("url_placeholder"),
            font=ctk.CTkFont(size=13),
            height=36
        )
        self.entry_url.grid(row=1, column=0, padx=(14, 6), pady=(0, 8), sticky="ew")
        self.entry_url.bind("<Return>", lambda event: self.add_single_url())

        # 加入按鈕
        self.btn_add = ctk.CTkButton(
            add_frame,
            text=i18n.t("btn_add"),
            font=ctk.CTkFont(size=13, weight="bold"),
            width=100,
            height=36,
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self.add_single_url
        )
        self.btn_add.grid(row=1, column=1, padx=4, pady=(0, 8))

        # 貼上剪貼簿按鈕
        self.btn_paste = ctk.CTkButton(
            add_frame,
            text=i18n.t("btn_paste"),
            width=100,
            height=36,
            fg_color="#334155",
            hover_color="#475569",
            command=self.paste_from_clipboard
        )
        self.btn_paste.grid(row=1, column=2, padx=4, pady=(0, 8))

        # 範例按鈕
        self.btn_sample = ctk.CTkButton(
            add_frame,
            text=i18n.t("btn_sample"),
            width=85,
            height=36,
            fg_color="#334155",
            hover_color="#475569",
            command=self.add_sample_song
        )
        self.btn_sample.grid(row=1, column=3, padx=(4, 14), pady=(0, 8))

        # ================= 3. 下載路徑、格式與編號設定區 =================
        settings_frame = ctk.CTkFrame(self, corner_radius=10)
        settings_frame.grid(row=2, column=0, padx=15, pady=4, sticky="ew")
        settings_frame.grid_columnconfigure(1, weight=1)

        # 第 1 列：儲存目錄與隨身碟捷徑
        self.lbl_dir = ctk.CTkLabel(settings_frame, text=i18n.t("lbl_save_dir"), font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_dir.grid(row=0, column=0, padx=(14, 6), pady=(8, 4), sticky="w")

        self.entry_dir = ctk.CTkEntry(settings_frame, font=ctk.CTkFont(size=12))
        self.entry_dir.insert(0, self.default_download_dir)
        self.entry_dir.grid(row=0, column=1, padx=6, pady=(8, 4), sticky="ew")

        self.btn_browse = ctk.CTkButton(
            settings_frame,
            text=i18n.t("btn_browse"),
            width=70,
            fg_color="#475569",
            command=self.browse_directory
        )
        self.btn_browse.grid(row=0, column=2, padx=4, pady=(8, 4))

        self.btn_usb = ctk.CTkButton(
            settings_frame,
            text=i18n.t("btn_usb"),
            width=85,
            fg_color="#0369a1",
            hover_color="#0284c7",
            command=self.quick_select_usb
        )
        self.btn_usb.grid(row=0, column=3, padx=4, pady=(8, 4))

        self.btn_open_folder = ctk.CTkButton(
            settings_frame,
            text=i18n.t("btn_open_folder"),
            width=65,
            fg_color="#475569",
            command=self.open_download_folder
        )
        self.btn_open_folder.grid(row=0, column=4, padx=(4, 14), pady=(8, 4))

        # 第 2 列：隨身碟/資料夾 001 編號智慧檢查列
        num_box = ctk.CTkFrame(settings_frame, fg_color="transparent")
        num_box.grid(row=1, column=0, columnspan=5, padx=14, pady=(0, 4), sticky="ew")

        self.chk_numbering = ctk.CTkCheckBox(
            num_box,
            text=i18n.t("chk_auto_number"),
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._on_numbering_toggled
        )
        self.chk_numbering.pack(side="left", padx=(0, 10))

        self.btn_check_format = ctk.CTkButton(
            num_box,
            text=i18n.t("btn_check_format"),
            width=190,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="#334155",
            hover_color="#475569",
            command=lambda: self.inspect_folder_format(user_triggered=True)
        )
        self.btn_check_format.pack(side="left", padx=4)

        self.lbl_num_info = ctk.CTkLabel(
            num_box,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="#38bdf8"
        )
        self.lbl_num_info.pack(side="left", padx=10)

        # 多線程併發下拉選單
        self.opt_threads = ctk.CTkOptionMenu(
            num_box,
            values=["5 線程 (極速/推薦)", "4 線程 (高速)", "3 線程 (標準)", "2 線程", "1 線程 (單工)"],
            width=135,
            height=28
        )
        self.opt_threads.set("5 線程 (極速/推薦)")
        self.opt_threads.pack(side="right", padx=(2, 0))

        self.lbl_threads = ctk.CTkLabel(
            num_box,
            text=i18n.t("lbl_threads"),
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_threads.pack(side="right", padx=(8, 2))

        # 第 3 列：類型切換 (音訊 / 視訊)、格式選單、品質設定與格式工廠轉檔工具
        opts_box = ctk.CTkFrame(settings_frame, fg_color="transparent")
        opts_box.grid(row=2, column=0, columnspan=5, padx=14, pady=(0, 6), sticky="ew")

        self.lbl_type = ctk.CTkLabel(opts_box, text=i18n.t("lbl_media_type"), font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_type.pack(side="left", padx=(0, 4))

        self.seg_media_type = ctk.CTkSegmentedButton(
            opts_box,
            values=[i18n.t("type_audio"), i18n.t("type_video")],
            command=self._on_media_type_changed,
            width=160
        )
        self.seg_media_type.set(i18n.t("type_audio"))
        self.seg_media_type.pack(side="left", padx=(0, 10))

        self.lbl_format = ctk.CTkLabel(opts_box, text=i18n.t("lbl_format"), font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_format.pack(side="left", padx=(0, 4))

        self.opt_format = ctk.CTkOptionMenu(
            opts_box,
            values=AUDIO_FORMAT_OPTIONS,
            command=self._on_format_changed,
            width=150
        )
        self.opt_format.set(AUDIO_FORMAT_OPTIONS[0])
        self.opt_format.pack(side="left", padx=(0, 10))

        self.lbl_quality = ctk.CTkLabel(opts_box, text=i18n.t("lbl_quality"), font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_quality.pack(side="left", padx=(0, 4))

        self.opt_quality = ctk.CTkOptionMenu(
            opts_box,
            values=AUDIO_QUALITIES_LOSSY,
            width=170
        )
        self.opt_quality.pack(side="left", padx=(0, 10))

        self.chk_thumb = ctk.CTkCheckBox(opts_box, text=i18n.t("chk_thumb"), font=ctk.CTkFont(size=12))
        self.chk_thumb.select()
        self.chk_thumb.pack(side="left", padx=6)

        self.chk_meta = ctk.CTkCheckBox(opts_box, text=i18n.t("chk_meta"), font=ctk.CTkFont(size=12))
        self.chk_meta.select()
        self.chk_meta.pack(side="left", padx=6)

        self.btn_format_factory = ctk.CTkButton(
            opts_box,
            text=i18n.t("btn_format_factory"),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self.open_format_factory_dialog,
            height=30
        )
        self.btn_format_factory.pack(side="right", padx=(4, 0))

        # 恢復使用者偏好格式
        pref_fmt = self.app_config.get("preferred_format", "mp3").lower()
        if pref_fmt in ('mp4', 'mkv', 'webm', 'mov', 'avi'):
            self.seg_media_type.set(i18n.t("type_video"))
            self.opt_format.configure(values=VIDEO_FORMAT_OPTIONS)
            match_opt = next((o for o in VIDEO_FORMAT_OPTIONS if extract_format_code(o) == pref_fmt), VIDEO_FORMAT_OPTIONS[0])
            self.opt_format.set(match_opt)
        else:
            self.seg_media_type.set(i18n.t("type_audio"))
            self.opt_format.configure(values=AUDIO_FORMAT_OPTIONS)
            match_opt = next((o for o in AUDIO_FORMAT_OPTIONS if extract_format_code(o) == pref_fmt), AUDIO_FORMAT_OPTIONS[0])
            self.opt_format.set(match_opt)

        # ================= 4. 歌曲清單管理與滾動展示區 =================
        list_container = ctk.CTkFrame(self, corner_radius=10)
        list_container.grid(row=3, column=0, padx=15, pady=4, sticky="nsew")
        list_container.grid_columnconfigure(0, weight=1)
        list_container.grid_rowconfigure(1, weight=1)

        tool_bar = ctk.CTkFrame(list_container, fg_color="transparent")
        tool_bar.grid(row=0, column=0, padx=14, pady=(6, 4), sticky="ew")
        tool_bar.grid_columnconfigure(0, weight=1)

        self.lbl_stats = ctk.CTkLabel(
            tool_bar,
            text=i18n.t("stats_pattern").format(total=0, selected=0),
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#e2e8f0"
        )
        self.lbl_stats.pack(side="left")

        # 重新嘗試失敗項目按鈕 (預設隱藏，有失敗時顯示)
        self.btn_retry_failed = ctk.CTkButton(
            tool_bar,
            text=i18n.t("btn_retry_failed"),
            width=115,
            height=28,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.retry_failed_items
        )

        self.btn_clear_all = ctk.CTkButton(
            tool_bar,
            text=i18n.t("btn_clear_list"),
            width=75,
            height=28,
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.clear_song_list
        )
        self.btn_clear_all.pack(side="right", padx=(6, 0))

        self.btn_deselect_all = ctk.CTkButton(
            tool_bar,
            text=i18n.t("btn_deselect_all"),
            width=75,
            height=28,
            fg_color="#475569",
            command=self.deselect_all_songs
        )
        self.btn_deselect_all.pack(side="right", padx=6)

        self.btn_select_all = ctk.CTkButton(
            tool_bar,
            text=i18n.t("btn_select_all"),
            width=70,
            height=28,
            fg_color="#475569",
            command=self.select_all_songs
        )
        self.btn_select_all.pack(side="right", padx=6)

        self.scroll_list = ctk.CTkScrollableFrame(list_container, corner_radius=6)
        self.scroll_list.grid(row=1, column=0, padx=10, pady=(2, 8), sticky="nsew")
        self.scroll_list.grid_columnconfigure(1, weight=1)

        self.lbl_empty = ctk.CTkLabel(
            self.scroll_list,
            text=i18n.t("lbl_empty_list"),
            font=ctk.CTkFont(size=14),
            text_color="#64748b"
        )
        self.lbl_empty.pack(pady=35)

        # ================= 5. 命令模式即時終端 (Command Mode Log) =================
        self.cmd_frame = ctk.CTkFrame(self, corner_radius=10)
        self.cmd_frame.grid(row=4, column=0, padx=15, pady=4, sticky="ew")
        self.cmd_frame.grid_columnconfigure(0, weight=1)

        cmd_top = ctk.CTkFrame(self.cmd_frame, fg_color="transparent")
        cmd_top.grid(row=0, column=0, padx=12, pady=(6, 2), sticky="ew")
        cmd_top.grid_columnconfigure(0, weight=1)

        self.lbl_cmd_title = ctk.CTkLabel(
            cmd_top,
            text=i18n.t("sec_cmd_console"),
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#38bdf8"
        )
        self.lbl_cmd_title.pack(side="left")

        self.chk_autoscroll = ctk.CTkCheckBox(cmd_top, text="自動滾動", font=ctk.CTkFont(size=11), width=18)
        self.chk_autoscroll.select()
        self.chk_autoscroll.pack(side="right", padx=(6, 0))

        btn_copy_log = ctk.CTkButton(
            cmd_top,
            text="📋 複製",
            width=60,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="#334155",
            hover_color="#475569",
            command=self.copy_log_to_clipboard
        )
        btn_copy_log.pack(side="right", padx=4)

        self.btn_clear_log = ctk.CTkButton(
            cmd_top,
            text=i18n.t("btn_clear_log"),
            width=60,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="#334155",
            hover_color="#475569",
            command=self.clear_log
        )
        self.btn_clear_log.pack(side="right", padx=4)

        self.btn_toggle_cmd = ctk.CTkButton(
            cmd_top,
            text="收合 ▲",
            width=55,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="#1e293b",
            hover_color="#334155",
            command=self.toggle_command_console
        )
        self.btn_toggle_cmd.pack(side="right", padx=4)

        self.txt_cmd = ctk.CTkTextbox(
            self.cmd_frame,
            height=110,
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#090d16",
            text_color="#e2e8f0"
        )
        self.txt_cmd.grid(row=1, column=0, padx=10, pady=(2, 4), sticky="ew")

        # 指令輸入列 (CLI Prompt)
        self.cmd_input_box = ctk.CTkFrame(self.cmd_frame, fg_color="transparent")
        self.cmd_input_box.grid(row=2, column=0, padx=10, pady=(0, 6), sticky="ew")
        self.cmd_input_box.grid_columnconfigure(1, weight=1)

        prompt_lbl = ctk.CTkLabel(
            self.cmd_input_box,
            text="❯",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#10b981",
            width=18
        )
        prompt_lbl.grid(row=0, column=0, padx=(2, 4), sticky="w")

        self.cmd_input = ctk.CTkEntry(
            self.cmd_input_box,
            placeholder_text="輸入指令 (輸入 'help' 查看指令清單，支援 ↑/↓ 歷史紀錄)...",
            font=ctk.CTkFont(family="Consolas", size=12),
            height=28
        )
        self.cmd_input.grid(row=0, column=1, padx=(0, 6), sticky="ew")
        self.cmd_input.bind("<Return>", lambda event: self.handle_console_command())
        self.cmd_input.bind("<Up>", self._on_cmd_history_up)
        self.cmd_input.bind("<Down>", self._on_cmd_history_down)

        self.btn_exec_cmd = ctk.CTkButton(
            self.cmd_input_box,
            text="執行",
            width=50,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#0284c7",
            hover_color="#0369a1",
            command=self.handle_console_command
        )
        self.btn_exec_cmd.grid(row=0, column=2, sticky="e")

        # ================= 6. 底部執行、進度條與控制列 =================
        bottom_frame = ctk.CTkFrame(self, corner_radius=10)
        bottom_frame.grid(row=5, column=0, padx=15, pady=(4, 12), sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)

        self.lbl_status = ctk.CTkLabel(
            bottom_frame,
            text=i18n.t("status_ready"),
            font=ctk.CTkFont(size=12),
            text_color="#94a3b8",
            anchor="w"
        )
        self.lbl_status.grid(row=0, column=0, padx=15, pady=(6, 2), sticky="ew")

        self.prog_bar = ctk.CTkProgressBar(bottom_frame)
        self.prog_bar.set(0)
        self.prog_bar.grid(row=1, column=0, padx=15, pady=3, sticky="ew")

        # 按鈕容器（包含主下載按鈕與暫停/停止控制，三合一常駐顯示）
        self.action_box = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        self.action_box.grid(row=2, column=0, padx=15, pady=(4, 8), sticky="ew")
        self.action_box.grid_columnconfigure(0, weight=6)
        self.action_box.grid_columnconfigure(1, weight=2)
        self.action_box.grid_columnconfigure(2, weight=2)

        # 1. 開始下載按鈕
        self.btn_download = ctk.CTkButton(
            self.action_box,
            text=i18n.t("btn_start_download_mp3"),
            font=ctk.CTkFont(size=15, weight="bold"),
            height=42,
            fg_color="#10b981",
            hover_color="#059669",
            command=self.start_download_batch
        )
        self.btn_download.grid(row=0, column=0, padx=(0, 6), sticky="ew")

        # 2. 暫停 / 繼續按鈕 (永久可見，未執行時 disabled)
        self.btn_pause = ctk.CTkButton(
            self.action_box,
            text=i18n.t("btn_pause"),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=42,
            fg_color="#334155",
            hover_color="#d97706",
            state="disabled",
            command=self.toggle_pause
        )
        self.btn_pause.grid(row=0, column=1, padx=3, sticky="ew")

        # 3. 停止下載按鈕 (永久可見，未執行時 disabled)
        self.btn_cancel = ctk.CTkButton(
            self.action_box,
            text=i18n.t("btn_cancel"),
            font=ctk.CTkFont(size=14, weight="bold"),
            height=42,
            fg_color="#334155",
            hover_color="#dc2626",
            state="disabled",
            command=self.cancel_download
        )
        self.btn_cancel.grid(row=0, column=2, padx=(6, 0), sticky="ew")

        # 底部版權宣告列
        lbl_footer = ctk.CTkLabel(
            bottom_frame,
            text="© 2026 The StreamForge Team & Contributors. All Rights Reserved. · MIT Open Source License",
            font=ctk.CTkFont(size=11),
            text_color="#64748b"
        )
        lbl_footer.grid(row=3, column=0, padx=15, pady=(2, 6))

        # 完成整體介面建置後，初始化格式與品質聯動
        if hasattr(self, "opt_format"):
            self._on_format_changed(self.opt_format.get())

    def show_about_dialog(self):
        AboutDialog(self)

    # ================= 多國語言介面即時切換 =================

    def _on_change_language(self, lang_name: str):
        """切換介面語言並即時刷新所有文字"""
        lang_code = i18n.LANG_CODE_MAP.get(lang_name, "zh_TW")
        i18n.set_current_language(lang_code)
        self.app_config["language"] = lang_code
        save_app_config(self.app_config)
        self.refresh_ui_texts()
        self.log(f"🌐 {i18n.t('lang_switched')} {lang_name} ({lang_code})")

    def refresh_ui_texts(self):
        """動態更新主介面上所有標籤、按鈕與提示文字"""
        curr_lang = i18n.get_current_language()
        curr_lang_name = i18n.LANGUAGES.get(curr_lang, "繁體中文")

        # 視窗與頂部標題
        self.title(f"StreamForge v{APP_VERSION} · {i18n.t('app_subtitle')}")
        self.title_lbl.configure(text=i18n.t("app_title"))
        self.sub_lbl.configure(text=i18n.t("app_subtitle"))
        self.btn_about.configure(text=i18n.t("btn_about"))
        self.opt_lang.set(curr_lang_name)

        # 區塊 1: 新增
        self.input_title.configure(text=i18n.t("sec_add_song"))
        self.entry_url.configure(placeholder_text=i18n.t("url_placeholder"))
        self.btn_add.configure(text=i18n.t("btn_add"))
        self.btn_paste.configure(text=i18n.t("btn_paste"))
        self.btn_sample.configure(text=i18n.t("btn_sample"))

        # 區塊 2: 設定
        self.lbl_dir.configure(text=i18n.t("lbl_save_dir"))
        self.btn_browse.configure(text=i18n.t("btn_browse"))
        self.btn_usb.configure(text=i18n.t("btn_usb"))
        self.btn_open_folder.configure(text=i18n.t("btn_open_folder"))
        self.chk_numbering.configure(text=i18n.t("chk_auto_number"))
        self.btn_check_format.configure(text=i18n.t("btn_check_format"))
        self.lbl_type.configure(text=i18n.t("lbl_media_type"))
        self.seg_media_type.configure(values=[i18n.t("type_audio"), i18n.t("type_video")])
        self.lbl_format.configure(text=i18n.t("lbl_format"))
        self.btn_format_factory.configure(text=i18n.t("btn_format_factory"))

        fmt = extract_format_code(self.opt_format.get())
        if fmt in ('mp4', 'mkv', 'webm', 'mov', 'avi'):
            self.lbl_quality.configure(text=i18n.t("lbl_quality_video"))
        else:
            self.lbl_quality.configure(text=i18n.t("lbl_quality_audio"))

        self.btn_download.configure(text=i18n.t("btn_start_download_pattern").format(fmt=fmt.upper()))
        self.chk_thumb.configure(text=i18n.t("chk_thumb"))
        self.chk_meta.configure(text=i18n.t("chk_meta"))

        # 區塊 3: 清單
        self.btn_select_all.configure(text=i18n.t("btn_select_all"))
        self.btn_deselect_all.configure(text=i18n.t("btn_deselect_all"))
        self.btn_clear_all.configure(text=i18n.t("btn_clear_list"))
        self.btn_retry_failed.configure(text=i18n.t("btn_retry_failed"))
        self.lbl_empty.configure(text=i18n.t("lbl_empty_list"))
        self.update_stats()

        # 區塊 4: 命令終端
        self.lbl_cmd_title.configure(text=i18n.t("sec_cmd_console"))
        self.btn_clear_log.configure(text=i18n.t("btn_clear_log"))
        self.btn_toggle_cmd.configure(text=i18n.t("btn_collapse") if self.console_visible else i18n.t("btn_expand"))

        # 區塊 5: 底部控制
        if not self.is_running:
            self.lbl_status.configure(text=i18n.t("status_ready"))
        if hasattr(self, 'lbl_threads') and self.lbl_threads:
            self.lbl_threads.configure(text=i18n.t("lbl_threads"))
        self.btn_pause.configure(text=i18n.t("btn_pause") if not self.is_paused else i18n.t("btn_resume"))
        self.btn_cancel.configure(text=i18n.t("btn_cancel"))

    # ================= 命令模式日誌功能 (帶佇列限頻，杜絕介面卡頓) =================

    def log(self, msg: str):
        """線程安全的即時日誌紀錄 (以 200ms 批次刷新，防止大量網絡數據包卡死 UI)"""
        now_str = datetime.now().strftime("%H:%M:%S")
        line = f"[{now_str}] {msg}\n"
        with self._log_lock:
            self._log_queue.append(line)
            if not self._log_flushing:
                self._log_flushing = True
                self.after(200, self._flush_log_queue)

    def _flush_log_queue(self):
        with self._log_lock:
            if not self._log_queue:
                self._log_flushing = False
                return
            batch = "".join(self._log_queue)
            self._log_queue.clear()
            self._log_flushing = False

        if hasattr(self, 'txt_cmd') and self.txt_cmd.winfo_exists():
            if getattr(self, 'console_visible', True):
                self.txt_cmd.insert("end", batch)
                try:
                    line_count = int(self.txt_cmd.index("end-1c").split('.')[0])
                    if line_count > 1500:
                        self.txt_cmd.delete("1.0", f"{line_count - 1000}.0")
                except Exception:
                    pass
                if getattr(self, 'chk_autoscroll', None) and self.chk_autoscroll.get():
                    self.txt_cmd.see("end")
            else:
                self.txt_cmd.insert("end", batch)

    def clear_log(self):
        with self._log_lock:
            self._log_queue.clear()
        self.txt_cmd.delete("1.0", "end")

    def copy_log_to_clipboard(self):
        try:
            content = self.txt_cmd.get("1.0", "end").strip()
            if content:
                self.clipboard_clear()
                self.clipboard_append(content)
                messagebox.showinfo("提示", "已將命令列日誌複製至剪貼簿！")
            else:
                messagebox.showinfo("提示", "日誌目前是空的。")
        except Exception as ex:
            messagebox.showerror("錯誤", f"複製失敗：{ex}")

    def toggle_command_console(self):
        if self.console_visible:
            self.txt_cmd.grid_remove()
            self.cmd_input_box.grid_remove()
            self.btn_toggle_cmd.configure(text="展開 ▼")
            self.console_visible = False
        else:
            self.txt_cmd.grid(row=1, column=0, padx=10, pady=(2, 4), sticky="ew")
            self.cmd_input_box.grid(row=2, column=0, padx=10, pady=(0, 6), sticky="ew")
            self.btn_toggle_cmd.configure(text="收合 ▲")
            self.console_visible = True

    # ================= 終端機指令互動邏輯 (CLI System) =================

    def _on_cmd_history_up(self, event):
        if not self.cmd_history:
            return "break"
        if self.cmd_history_idx == -1:
            self.cmd_history_idx = len(self.cmd_history) - 1
        elif self.cmd_history_idx > 0:
            self.cmd_history_idx -= 1
        
        self.cmd_input.delete(0, tk.END)
        self.cmd_input.insert(0, self.cmd_history[self.cmd_history_idx])
        return "break"

    def _on_cmd_history_down(self, event):
        if not self.cmd_history:
            return "break"
        if self.cmd_history_idx != -1:
            if self.cmd_history_idx < len(self.cmd_history) - 1:
                self.cmd_history_idx += 1
                self.cmd_input.delete(0, tk.END)
                self.cmd_input.insert(0, self.cmd_history[self.cmd_history_idx])
            else:
                self.cmd_history_idx = -1
                self.cmd_input.delete(0, tk.END)
        return "break"

    def handle_console_command(self):
        raw_cmd = self.cmd_input.get().strip()
        if not raw_cmd:
            return

        self.cmd_input.delete(0, tk.END)
        self.cmd_history.append(raw_cmd)
        self.cmd_history_idx = -1

        self.log(f"❯ {raw_cmd}")

        parts = raw_cmd.split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ("help", "?", "h"):
            self._cli_help()
        elif cmd in ("add", "a"):
            self._cli_add(args)
        elif cmd in ("paste", "p"):
            self.paste_from_clipboard()
        elif cmd in ("list", "ls"):
            self._cli_list()
        elif cmd in ("select", "sel"):
            self._cli_select(args)
        elif cmd in ("del", "rm", "delete"):
            self._cli_delete(args)
        elif cmd in ("start", "dl", "run", "download"):
            self._cli_start()
        elif cmd == "pause":
            self._cli_pause()
        elif cmd == "resume":
            self._cli_resume()
        elif cmd in ("cancel", "stop"):
            self._cli_cancel()
        elif cmd in ("retry", "r"):
            self._cli_retry()
        elif cmd in ("format", "fmt"):
            self._cli_format(args)
        elif cmd in ("quality", "q"):
            self._cli_quality(args)
        elif cmd in ("convert", "factory"):
            self.open_format_factory_dialog()
        elif cmd in ("dir", "cd"):
            self._cli_dir(args)
        elif cmd == "usb":
            self.quick_select_usb()
        elif cmd == "check":
            self.inspect_folder_format(user_triggered=True)
        elif cmd in ("number", "num"):
            self._cli_number(args)
        elif cmd in ("about", "copyright", "author", "team"):
            self._cli_about()
        elif cmd in ("update", "check-update", "upgrade"):
            self.log("🔍 正在連線檢查 StreamForge 最新發布版本...")
            check_for_updates(parent=self, silent=False)
        elif cmd == "open":
            self.open_download_folder()
        elif cmd == "status":
            self._cli_status()
        elif cmd in ("clear", "cls"):
            self.clear_log()
        elif cmd in ("exit", "quit"):
            self.destroy()
        else:
            self.log(f"❌ [CLI 錯誤] 未知指令: '{cmd}'。輸入 'help' 查看所有可用指令。")

    def _cli_about(self):
        banner = (
            "=========================================================\n"
            "  ⚡ StreamForge v1.0.0 (Release Build)\n"
            "  High-Performance Media Stream & Audio Processing Utility\n\n"
            "  © 2026 The StreamForge Team & Contributors.\n"
            "  All Rights Reserved. 保留所有權利。\n\n"
            "  Licensed under the MIT License.\n"
            "  For personal research, study, and fair-use only.\n"
            "========================================================="
        )
        self.log(banner)

    def _cli_help(self):
        help_text = (
            "================== 💻 終端機控制台可用指令 ==================\n"
            "  about / copyright         : 顯示 StreamForge 軟體版本與智慧財產權宣告\n"
            "  update / check-update     : 檢查 StreamForge 最新版本與更新\n"
            "  add <網址> / a <網址>       : 加入單曲或播放清單網址至清單\n"
            "  paste / p                 : 從剪貼簿讀取網址並加入\n"
            "  list / ls                 : 列出當前清單所有歌曲與下載狀態\n"
            "  select <all|none|編號...>  : 選取或反選 (如: select all, select 1 3)\n"
            "  del <all|編號...> / rm     : 從清單中刪除歌曲 (如: del 2, del all)\n"
            "  start / dl / run          : 開始批次下載所有已勾選的歌曲\n"
            "  pause                     : 暫停當前下載任務\n"
            "  resume                    : 恢復已暫停的下載任務\n"
            "  cancel / stop             : 取消當前的下載任務\n"
            "  format <格式> / fmt       : 切換輸出格式 (mp3, wav, flac, m4a, aac, ogg, opus, mp4, mkv, webm, mov, avi)\n"
            "  quality <數值> / q <數值>  : 設定音質(320/256/192/128/lossless)或畫質(4k/2k/1080/720/480)\n"
            "  convert / factory         : 開啟本地格式工廠 (批次媒體轉檔工具)\n"
            "  dir [路徑] / cd [路徑]     : 顯示或更換下載儲存目錄\n"
            "  usb                       : 自動偵測並切換至 USB 隨身碟\n"
            "  check                     : 檢查資料夾中的 001 編號格式\n"
            "  number <on|off>           : 開啟或關閉 001 檔名前綴順序編號\n"
            "  open                      : 在檔案總管中開啟當前下載目錄\n"
            "  status                    : 顯示目前設定與清單統計摘要\n"
            "  clear / cls               : 清除終端機畫面\n"
            "  exit / quit               : 關閉程式\n"
            "========================================================="
        )
        self.log(help_text)

    def _cli_add(self, args):
        if not args:
            self.log("⚠️ [CLI 提示] 請在指令後帶入網址，例如: add https://www.youtube.com/watch?v=...")
            return
        url = args[0]
        self.entry_url.delete(0, tk.END)
        self.entry_url.insert(0, url)
        self.add_single_url()

    def _cli_list(self):
        if not self.songs:
            self.log("📭 [CLI] 清單目前是空的。可使用 'add <網址>' 加入歌曲。")
            return
        self.log(f"📋 [CLI] 當前清單共 {len(self.songs)} 首歌曲：")
        for i, s in enumerate(self.songs, 1):
            chk = "✓" if s['var'].get() else " "
            status_txt = s.get('status', '等待中')
            if 'status_lbl' in s and s['status_lbl'].winfo_exists():
                status_txt = s['status_lbl'].cget("text")
            self.log(f"  [{chk}] {i:02d}. {s['title']} ({s['duration_str']}) [{status_txt}]")

    def _cli_select(self, args):
        if not args or args[0].lower() in ("all", "a", "*"):
            self.select_all_songs()
            self.log("✅ [CLI] 已全選清單中所有歌曲。")
        elif args[0].lower() in ("none", "no", "clear", "0"):
            self.deselect_all_songs()
            self.log("⬜ [CLI] 已取消勾選所有歌曲。")
        else:
            indices = set()
            for arg in args:
                if "-" in arg:
                    parts = arg.split("-")
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                        start, end = int(parts[0]), int(parts[1])
                        for n in range(start, end + 1):
                            indices.add(n)
                elif arg.isdigit():
                    indices.add(int(arg))

            if not indices:
                self.log("⚠️ [CLI 提示] 無效的選取參數。用法: select all 或 select 1 2 3 或 select 1-5")
                return

            for i, s in enumerate(self.songs, 1):
                s['var'].set(i in indices)
            self.update_stats()
            self.log(f"✅ [CLI] 已選取指定編號的項目: {sorted(list(indices))}")

    def _cli_delete(self, args):
        if not args:
            self.log("⚠️ [CLI 提示] 請指定要刪除的歌曲編號或 all，例如: del 2 或 del all")
            return
        if args[0].lower() in ("all", "clear"):
            self.clear_song_list()
        else:
            to_remove_indices = []
            for arg in args:
                if arg.isdigit():
                    idx = int(arg) - 1
                    if 0 <= idx < len(self.songs):
                        to_remove_indices.append(idx)

            if not to_remove_indices:
                self.log("⚠️ [CLI 提示] 找不到指定的歌曲編號。")
                return

            to_remove_indices.sort(reverse=True)
            for idx in to_remove_indices:
                s = self.songs[idx]
                rf = s.get('row_widget')
                self.remove_single_song(s, rf)
            self.log(f"🗑️ [CLI] 已從清單刪除指定項目。")

    def _cli_start(self):
        if self.is_running:
            self.log("⚠️ [CLI] 任務已在執行中！")
            return
        self.start_download_batch()

    def _cli_pause(self):
        if not self.is_running:
            self.log("⚠️ [CLI] 目前沒有正在執行的下載任務。")
            return
        if not self.is_paused:
            self.toggle_pause()
        else:
            self.log("ℹ️ [CLI] 下載任務目前已是暫停狀態。")

    def _cli_resume(self):
        if not self.is_running:
            self.log("⚠️ [CLI] 目前沒有正在執行的下載任務。")
            return
        if self.is_paused:
            self.toggle_pause()
        else:
            self.log("ℹ️ [CLI] 下載任務目前正在執行中，未處於暫停狀態。")

    def _cli_cancel(self):
        if not self.is_running:
            self.log("⚠️ [CLI] 目前沒有正在執行的下載任務。")
            return
        self.cancel_download()

    def _cli_retry(self):
        self.retry_failed_items()

    def _cli_format(self, args):
        if not args:
            curr = self.opt_format.get()
            self.log(f"ℹ️ [CLI] 目前輸出格式為: {curr}。可用格式: mp3, m4a, wav, flac, aac, ogg, opus, mp4, mkv, webm, mov, avi")
            return
        target = args[0].lower().strip()
        matched = False
        for opt in VIDEO_FORMAT_OPTIONS:
            if extract_format_code(opt) == target:
                self.seg_media_type.set(i18n.t("type_video"))
                self.opt_format.configure(values=VIDEO_FORMAT_OPTIONS)
                self.opt_format.set(opt)
                self._on_format_changed(opt)
                self.log(f"🎬 [CLI] 輸出格式已切換為: {opt}")
                matched = True
                break
        if not matched:
            for opt in AUDIO_FORMAT_OPTIONS:
                if extract_format_code(opt) == target:
                    self.seg_media_type.set(i18n.t("type_audio"))
                    self.opt_format.configure(values=AUDIO_FORMAT_OPTIONS)
                    self.opt_format.set(opt)
                    self._on_format_changed(opt)
                    self.log(f"🎵 [CLI] 輸出格式已切換為: {opt}")
                    matched = True
                    break
        if not matched:
            self.log(f"⚠️ [CLI 錯誤] 未知的格式: {target}。可用音訊: mp3, m4a, wav, flac, aac, ogg, opus；可用視訊: mp4, mkv, webm, mov, avi")

    def _cli_quality(self, args):
        if not args:
            curr = self.opt_quality.get()
            self.log(f"ℹ️ [CLI] 目前品質設定為: {curr}")
            return
        val = args[0].lower()
        fmt = extract_format_code(self.opt_format.get())
        if fmt in ('mp4', 'mkv', 'webm', 'mov', 'avi'):
            mapping = {
                "4k": "2160p (4K Ultra HD)",
                "2160": "2160p (4K Ultra HD)",
                "2k": "1440p (2K Quad HD)",
                "1440": "1440p (2K Quad HD)",
                "best": "最高畫質 (最佳/推薦)",
                "max": "最高畫質 (最佳/推薦)",
                "1080": "1080p (Full HD)",
                "1080p": "1080p (Full HD)",
                "720": "720p (HD)",
                "720p": "720p (HD)",
                "480": "480p (標清)",
                "480p": "480p (標清)",
                "360": "360p (節省空間)",
                "360p": "360p (節省空間)",
            }
            if val in mapping:
                self.opt_quality.set(mapping[val])
                self.log(f"📺 [CLI] 影片畫質已設定為: {mapping[val]}")
            else:
                self.log("⚠️ [CLI 錯誤] 可用畫質: best, 2160, 1440, 1080, 720, 480, 360")
        elif fmt in ('wav', 'flac'):
            self.opt_quality.set("無損音質 (Lossless / 原音還原)")
            self.log("💿 [CLI] WAV/FLAC 固定為無損音質")
        else:
            mapping = {
                "320": "320 kbps (最高品質/推薦)",
                "320k": "320 kbps (最高品質/推薦)",
                "256": "256 kbps (高質量)",
                "256k": "256 kbps (高質量)",
                "192": "192 kbps (標準)",
                "192k": "192 kbps (標準)",
                "128": "128 kbps (輕巧)",
                "128k": "128 kbps (輕巧)",
            }
            if val in mapping:
                self.opt_quality.set(mapping[val])
                self.log(f"🎧 [CLI] 音訊位元率已設定為: {mapping[val]}")
            else:
                self.log("⚠️ [CLI 錯誤] 可用音質: 320, 256, 192, 128")

    def _cli_dir(self, args):
        if not args:
            self.log(f"📁 [CLI] 目前下載儲存目錄為: {self.entry_dir.get()}")
            return
        new_dir = " ".join(args).strip('"').strip("'")
        if not os.path.exists(new_dir):
            try:
                os.makedirs(new_dir, exist_ok=True)
            except Exception as ex:
                self.log(f"❌ [CLI 錯誤] 無法建立目錄: {ex}")
                return
        self.entry_dir.delete(0, tk.END)
        self.entry_dir.insert(0, new_dir)
        self.log(f"📁 [CLI] 下載目錄已更換為: {new_dir}")
        self.inspect_folder_format(user_triggered=False)

    def _cli_number(self, args):
        if not args:
            curr = "開啟" if self.chk_numbering.get() else "關閉"
            self.log(f"🔢 [CLI] 檔名前綴 001 編號功能目前為: {curr}。可用指令: number on 或 number off")
            return
        state = args[0].lower()
        if state in ("on", "1", "true", "yes"):
            self.chk_numbering.select()
            self._on_numbering_toggled()
            self.log("🔢 [CLI] 已開啟 001 編號功能。")
        elif state in ("off", "0", "false", "no"):
            self.chk_numbering.deselect()
            self._on_numbering_toggled()
            self.log("🔢 [CLI] 已關閉 001 編號功能。")
        else:
            self.log("⚠️ [CLI 錯誤] 請輸入: number on 或 number off")

    def _cli_status(self):
        total = len(self.songs)
        selected = sum(1 for s in self.songs if s['var'].get())
        failed = sum(1 for s in self.songs if s.get('error'))
        running_str = "下載中" if self.is_running else ("暫停中" if self.is_paused else "閒置")
        num_str = f"開啟 (接續至 {self.next_number:03d})" if self.chk_numbering.get() else "關閉"
        status_msg = (
            "================== 📊 系統當前狀態摘要 ==================\n"
            f"  執行狀態: {running_str}\n"
            f"  歌曲清單: 共 {total} 首 (已勾選 {selected} 首 | 失敗 {failed} 首)\n"
            f"  輸出格式: {self.opt_format.get()}\n"
            f"  輸出品質: {self.opt_quality.get()}\n"
            f"  順序編號: {num_str}\n"
            f"  儲存目錄: {self.entry_dir.get()}\n"
            "========================================================="
        )
        self.log(status_msg)

    # ================= 隨身碟與資料夾編號智慧檢查 =================

    def _detect_usb_drives(self):
        drives = downloader.get_removable_drives()
        if drives:
            self.btn_usb.configure(text=f"💾 隨身碟 ({drives[0][0]}:)")
            self.log(f"💾 偵測到可用的隨身碟代號: {', '.join(drives)}")
        else:
            self.btn_usb.configure(text="💾 隨身碟")

    def quick_select_usb(self):
        drives = downloader.get_removable_drives()
        if not drives:
            messagebox.showinfo("提示", "目前未偵測到插入的 USB 隨身碟！\n請插入隨身碟後再次點擊，或使用「瀏覽」按鈕手動選擇。")
            return

        target = drives[0]
        self.entry_dir.delete(0, tk.END)
        self.entry_dir.insert(0, target)
        self.lbl_status.configure(text=f"已選取隨身碟: {target}")
        self.log(f"已切換下載目標為隨身碟: {target}")
        self.inspect_folder_format(user_triggered=False)

    def _on_numbering_toggled(self):
        if self.chk_numbering.get():
            self.inspect_folder_format(user_triggered=False)
        else:
            self.lbl_num_info.configure(text="（不加入編號）")

    def inspect_folder_format(self, user_triggered=False):
        folder_path = self.entry_dir.get().strip()
        if not os.path.exists(folder_path):
            return

        res = downloader.check_folder_numbering(folder_path)

        if res['status'] == 'empty':
            self.next_number = 1
            if self.chk_numbering.get():
                self.lbl_num_info.configure(text="（資料夾為空，新檔案將從 001 開始）")
            if user_triggered:
                messagebox.showinfo("檢查結果", f"資料夾為空或無現有音訊/影片檔案。\n新下載項目若啟用編號，將由 001 開始。")

        elif res['status'] == 'already_numbered':
            self.next_number = res['next_number']
            self.chk_numbering.select()
            self.lbl_num_info.configure(text=f"（已編號至 {res['next_number']-1:03d}，新檔將從 {self.next_number:03d} 開始）")
            if user_triggered:
                messagebox.showinfo(
                    "格式正確",
                    f"✅ 目標資料夾已完全符合 001, 002... 編號格式！\n"
                    f"現有歌曲: {res['total_files']} 首\n"
                    f"後續新下載將自動接續編號（由 {self.next_number:03d} 開始）。"
                )

        elif res['status'] == 'not_numbered':
            un_count = len(res['un_numbered_files'])
            total = res['total_files']

            msg = (
                f"【資料夾編號格式檢查】\n\n"
                f"目標路徑：{folder_path}\n"
                f"目前共有 {total} 個檔案，其中有 {un_count} 個尚未符合「001, 002...」編號格式。\n\n"
                f"請問您是否要將現有檔案全部重新編號命名（Rename），並讓後續下載的歌曲接續編號？\n\n"
                f"--------------------------------------------------\n"
                f"• 點擊【是 (Yes)】：\n"
                f"  系統將現有檔案全部重新命名為 001 - 檔名、002 - 檔名...\n"
                f"  新下載的歌曲將自動接續編號（從 {total+1:03d} 開始）！\n\n"
                f"• 點擊【否 (No)】：\n"
                f"  保持現有檔案名稱不變，且新下載的歌曲「不加上任何數字編號」。"
            )

            ans = messagebox.askyesno("格式檢查與重新命名", msg, parent=self)
            if ans:
                try:
                    self.next_number = downloader.rename_folder_files_to_numbered(folder_path, start_number=1)
                    self.chk_numbering.select()
                    self.lbl_num_info.configure(text=f"（已重新編號，新檔將從 {self.next_number:03d} 開始）")
                    self.log(f"✅ 目標資料夾現有 {total} 個檔案已全部重新編號命名完成！")
                    messagebox.showinfo("成功", f"🎉 現有 {total} 個檔案已全部重新編號命名完成！\n新下載的歌曲將由 {self.next_number:03d} 接續。")
                except Exception as ex:
                    self.log(f"❌ 重新命名現有檔案失敗: {ex}")
                    messagebox.showerror("錯誤", f"重新命名現有檔案時發生錯誤：\n{str(ex)}")
            else:
                self.chk_numbering.deselect()
                self.lbl_num_info.configure(text="（不加入編號）")

    # ================= 格式與媒體類型切換事件 =================

    def _on_media_type_changed(self, value):
        if "視訊" in value or "Video" in value or "Vídeo" in value or "動画" in value or "비디오" in value:
            self.opt_format.configure(values=VIDEO_FORMAT_OPTIONS)
            self.opt_format.set(VIDEO_FORMAT_OPTIONS[0])
            self._on_format_changed(VIDEO_FORMAT_OPTIONS[0])
        else:
            self.opt_format.configure(values=AUDIO_FORMAT_OPTIONS)
            self.opt_format.set(AUDIO_FORMAT_OPTIONS[0])
            self._on_format_changed(AUDIO_FORMAT_OPTIONS[0])

    def _on_format_changed(self, value):
        fmt = extract_format_code(value)
        if getattr(self, "lbl_quality", None) and getattr(self, "opt_quality", None):
            if fmt in ('wav', 'flac'):
                self.lbl_quality.configure(text=i18n.t("lbl_quality_audio"))
                self.opt_quality.configure(values=AUDIO_QUALITIES_LOSSLESS)
                self.opt_quality.set(AUDIO_QUALITIES_LOSSLESS[0])
                if getattr(self, "chk_thumb", None):
                    if fmt == 'wav':
                        self.chk_thumb.configure(state="disabled")
                    else:
                        self.chk_thumb.configure(state="normal")
                self.log(f"切換為 💿 {fmt.upper()} (無損音訊模式)")
            elif fmt in ('mp3', 'm4a', 'aac', 'ogg', 'opus'):
                self.lbl_quality.configure(text=i18n.t("lbl_quality_audio"))
                self.opt_quality.configure(values=AUDIO_QUALITIES_LOSSY)
                self.opt_quality.set(AUDIO_QUALITIES_LOSSY[0])
                if getattr(self, "chk_thumb", None):
                    self.chk_thumb.configure(state="normal" if fmt in ('mp3', 'm4a', 'ogg') else "disabled")
                self.log(f"切換為 🎵 {fmt.upper()} (純音訊模式)")
            else:
                self.lbl_quality.configure(text=i18n.t("lbl_quality_video"))
                self.opt_quality.configure(values=VIDEO_QUALITIES)
                self.opt_quality.set(VIDEO_QUALITIES[0])
                if getattr(self, "chk_thumb", None):
                    self.chk_thumb.configure(state="disabled")
                self.log(f"切換為 🎬 {fmt.upper()} (視訊影片模式)")

        if getattr(self, "btn_download", None):
            pattern = i18n.t("btn_start_download_pattern")
            self.btn_download.configure(text=pattern.format(fmt=fmt.upper()))

        # 記憶偏好格式
        self.app_config["preferred_format"] = fmt
        save_app_config(self.app_config)

    def open_format_factory_dialog(self):
        """開啟本地多媒體格式工廠轉檔視窗"""
        curr_dir = self.entry_dir.get().strip() or self.default_download_dir
        FormatFactoryDialog(self, default_out_dir=curr_dir, log_callback=self.log)

    # ================= 互動事件處理 =================

    def paste_from_clipboard(self):
        try:
            clip = self.clipboard_get().strip()
            if clip:
                self.entry_url.delete(0, tk.END)
                self.entry_url.insert(0, clip)
                self.add_single_url()
            else:
                messagebox.showinfo("提示", "剪貼簿目前沒有內容！")
        except Exception:
            messagebox.showinfo("提示", "無法從剪貼簿讀取網址！")

    def add_sample_song(self):
        sample = "https://www.youtube.com/watch?v=k85mRPqvMbE"
        self.entry_url.delete(0, tk.END)
        self.entry_url.insert(0, sample)
        self.add_single_url()

    def browse_directory(self):
        path = filedialog.askdirectory(title="選擇下載檔案儲存目錄", initialdir=self.entry_dir.get())
        if path:
            self.entry_dir.delete(0, tk.END)
            self.entry_dir.insert(0, path)
            self.app_config["download_dir"] = path
            save_app_config(self.app_config)
            self.log(f"已更換儲存目錄: {path}")
            self.inspect_folder_format(user_triggered=False)

    def open_download_folder(self):
        target = self.entry_dir.get().strip()
        if not os.path.exists(target):
            os.makedirs(target, exist_ok=True)
        try:
            os.startfile(target)
        except Exception as ex:
            self.log(f"開啟資料夾失敗: {ex}")
            messagebox.showerror("錯誤", f"無法開啟資料夾：{ex}")

    def update_stats(self):
        total = len(self.songs)
        selected = sum(1 for s in self.songs if s['var'].get())
        pattern = i18n.t("stats_pattern")
        self.lbl_stats.configure(text=pattern.format(total=total, selected=selected))

    def select_all_songs(self):
        for s in self.songs:
            s['var'].set(True)
        self.update_stats()

    def deselect_all_songs(self):
        for s in self.songs:
            s['var'].set(False)
        self.update_stats()

    def clear_song_list(self):
        if self.is_running:
            messagebox.showwarning("提示", "正在執行下載任務，無法清空清單！", parent=self)
            return
        if not self.songs:
            return
        if messagebox.askyesno("確認清空", "確定要清空目前清單中的所有歌曲嗎？", parent=self):
            for w in self.song_widgets:
                w.destroy()
            self.song_widgets.clear()
            self.songs.clear()
            self.lbl_empty.pack(pady=35)
            self.btn_retry_failed.pack_forget()
            self.update_stats()
            self.log("已清空歌曲清單。")

    def remove_single_song(self, song_item, row_frame):
        if self.is_running:
            messagebox.showwarning("提示", "正在執行下載任務，無法移除歌曲！", parent=self)
            return
        if song_item in self.songs:
            self.songs.remove(song_item)
        row_frame.destroy()
        if not self.songs:
            self.lbl_empty.pack(pady=35)
            self.btn_retry_failed.pack_forget()
        self.update_stats()

    def show_single_error_detail(self, song):
        """顯示單一歌曲失敗原因詳細視窗"""
        err_msg = song.get('error', '未知錯誤')
        msg = f"【下載失敗詳情】\n\n歌曲標題：{song['title']}\n網址：{song['url']}\n\n錯誤原因：\n{err_msg}\n\n是否立即單獨重新下載此首？"
        if messagebox.askyesno("失敗詳情與重試", msg, parent=self):
            for s in self.songs:
                s['var'].set(s == song)
            self.update_stats()
            self.start_download_batch()

    def render_song_row(self, item):
        self.lbl_empty.pack_forget()

        row = ctk.CTkFrame(self.scroll_list, corner_radius=6, fg_color="#1e293b")
        row.pack(fill="x", padx=4, pady=3)
        row.grid_columnconfigure(1, weight=1)

        # 勾選框
        var = tk.BooleanVar(value=item.get('selected', True))
        item['var'] = var
        item['row_widget'] = row

        chk = ctk.CTkCheckBox(row, text="", variable=var, width=24, command=self.update_stats)
        chk.grid(row=0, column=0, rowspan=2, padx=(10, 6), pady=8)

        # 歌曲名稱與資訊
        idx = len(self.songs)
        title_lbl = ctk.CTkLabel(
            row,
            text=f"{idx}. {item['title']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            text_color="#f8fafc"
        )
        title_lbl.grid(row=0, column=1, padx=4, pady=(6, 2), sticky="w")

        meta_lbl = ctk.CTkLabel(
            row,
            text=f"頻道: {item['uploader']}  |  長度: {item['duration_str']}",
            font=ctk.CTkFont(size=11),
            anchor="w",
            text_color="#94a3b8"
        )
        meta_lbl.grid(row=1, column=1, padx=4, pady=(0, 6), sticky="w")

        # 狀態標籤（點擊失敗可查看原因）
        status_lbl = ctk.CTkLabel(
            row,
            text="⏳ 等待中",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="#cbd5e1",
            width=110
        )
        status_lbl.grid(row=0, column=2, rowspan=2, padx=8, pady=8)
        status_lbl.bind("<Button-1>", lambda event, it=item: self._on_status_clicked(it))
        item['status_lbl'] = status_lbl

        # 刪除按鈕
        btn_del = ctk.CTkButton(
            row,
            text="✕",
            width=28,
            height=28,
            fg_color="#334155",
            hover_color="#ef4444",
            command=lambda it=item, rf=row: self.remove_single_song(it, rf)
        )
        btn_del.grid(row=0, column=3, rowspan=2, padx=(4, 10), pady=8)

        self.song_widgets.append(row)

    def _on_status_clicked(self, song):
        if song.get('error'):
            self.show_single_error_detail(song)

    # ================= 單條網址解析與加入 =================

    def add_single_url(self):
        raw_url = self.entry_url.get().strip()
        if not raw_url:
            messagebox.showwarning("提示", "請先輸入或貼上影音網址！")
            return

        if self.is_running:
            messagebox.showwarning("提示", "正在執行下載任務，請稍候再加入！")
            return

        self.entry_url.delete(0, tk.END)
        self.entry_url.focus_set()

        self.btn_add.configure(state="disabled", text="🔍 解析中...")
        self.lbl_status.configure(text=f"正在解析歌曲資訊: {raw_url[:50]}...")
        self.log(f"開始解析網址資訊: {raw_url}")
        self.prog_bar.set(0.2)

        threading.Thread(target=self._worker_add_url, args=(raw_url,), daemon=True).start()

    def _worker_add_url(self, url):
        items = downloader.extract_single_url_info(url)
        self.after(0, lambda: self._on_single_url_parsed(items, url))

    def _on_single_url_parsed(self, items, url):
        self.btn_add.configure(state="normal", text="➕ 加入清單")
        self.prog_bar.set(0)

        if not items:
            self.lbl_status.configure(text="解析失敗，請確認網址正確性。")
            self.log(f"❌ 解析失敗：無法讀取該網址 {url}")
            messagebox.showerror("錯誤", f"無法從網址解析出曲目：\n{url}", parent=self)
            return

        # 若網址解析出多首歌曲（播放清單 / 合輯），先跳出視窗確認是否匯入整個清單
        if len(items) > 1:
            first_title = items[0].get('title', '第一首歌曲')
            total_items = len(items)
            msg = (
                f"偵測到此網址包含播放清單（共 {total_items} 首歌曲）。\n\n"
                f"請問您是否要匯入整個播放清單？\n\n"
                f"--------------------------------------------------\n"
                f"• 點選【是 (Yes)】：\n"
                f"  匯入整個播放清單（全部 {total_items} 首歌曲）\n\n"
                f"• 點選【否 (No)】：\n"
                f"  僅匯入第 1 首歌曲至駐列清單\n"
                f"  （{first_title}）"
            )
            import_all = messagebox.askyesno("匯入播放清單確認", msg, parent=self)
            if not import_all:
                items = [items[0]]
                self.log(f"ℹ️ 使用者選擇僅匯入播放清單第 1 首歌曲: {first_title}")
            else:
                self.log(f"ℹ️ 使用者確認匯入整個播放清單（共 {total_items} 首歌曲）")

        existing_ids = {s['id'] for s in self.songs}
        valid_items = []
        for item in items:
            if item.get('status') == '解析失敗':
                self.log(f"❌ 解析曲目失敗: {item.get('error', '未知錯誤')}")
                messagebox.showerror("解析失敗", f"無法讀取該網址：\n{item.get('error', '未知錯誤')}", parent=self)
                continue
            if item['id'] not in existing_ids:
                valid_items.append(item)
                existing_ids.add(item['id'])

        if not valid_items:
            self.btn_add.configure(state="normal", text="➕ 加入清單")
            self.prog_bar.set(0)
            self.lbl_status.configure(text="⚠️ 該歌曲或清單項目已在清單中，未重複加入。")
            return

        total_new = len(valid_items)

        # 若項目只有 1~3 首，直接同步極速渲染
        if total_new <= 3:
            for item in valid_items:
                self.songs.append(item)
                self.render_song_row(item)
                self.log(f"➕ 已加入曲目: {item['title']} (頻道: {item['uploader']}, 長度: {item['duration_str']})")
            self.btn_add.configure(state="normal", text="➕ 加入清單")
            self.prog_bar.set(0)
            self.update_stats()
            if total_new == 1:
                self.lbl_status.configure(text=f"✅ 已成功加入: {valid_items[0]['title']}")
            else:
                self.lbl_status.configure(text=f"✅ 已成功加入 {total_new} 首歌曲！")
            return

        # 若為大量曲目（如播放清單），採用非同步微批次流水線渲染，每次渲染 8 首並讓出 UI 線程，杜絕介面卡死
        self.log(f"⚡ 正在以極速流水線加入 {total_new} 首歌曲至駐列清單...")

        def _render_chunk(start_idx):
            end_idx = min(start_idx + 8, total_new)
            for i in range(start_idx, end_idx):
                item = valid_items[i]
                self.songs.append(item)
                self.render_song_row(item)

            self.update_stats()
            pct = end_idx / total_new
            self.prog_bar.set(pct)
            self.lbl_status.configure(text=f"➕ 正在加入清單曲目 ({end_idx}/{total_new})...")

            if end_idx < total_new:
                self.after(5, lambda: _render_chunk(end_idx))
            else:
                self.btn_add.configure(state="normal", text="➕ 加入清單")
                self.prog_bar.set(0)
                self.lbl_status.configure(text=f"✅ 已成功從播放清單加入 {total_new} 首歌曲！")
                self.log(f"🎉 已成功將播放清單中全部 {total_new} 首歌曲加入駐列清單！")

        _render_chunk(0)

    # ================= 批次下載、暫停、取消與查重 =================

    def ask_duplicate_action(self, song_title: str, existing_filename: str):
        """線程安全的重複檔案確認視窗"""
        result = {'action': 'skip', 'apply_all': False}
        ev = threading.Event()

        def _show():
            dlg = DuplicateDialog(self, song_title, existing_filename)
            dlg.wait_window()
            result['action'] = dlg.action
            result['apply_all'] = dlg.apply_all
            ev.set()

        self.after(0, _show)
        ev.wait()
        return result['action'], result['apply_all']

    def get_selected_thread_count(self) -> int:
        """獲取使用者所選的多線程併發數量"""
        if hasattr(self, 'opt_threads') and self.opt_threads:
            val = self.opt_threads.get()
            digits = re.findall(r'\d+', val)
            if digits:
                return max(1, min(8, int(digits[0])))
        return 5

    def toggle_pause(self):
        """暫停或恢復下載"""
        if not self.is_running:
            return
        if self.is_paused:
            self.is_paused = False
            self.pause_event.set()
            self.btn_pause.configure(text=i18n.t("btn_pause"), fg_color="#f59e0b", hover_color="#d97706")
            self.lbl_status.configure(text="▶️ 恢復下載中...")
            self.log("▶️ 使用者恢復了下載任務")
            for s in self.songs:
                if s.get('status') == 'paused':
                    s['status'] = 'downloading'
                    self._update_song_status(s, "⚡ 下載中...", "#f59e0b")
        else:
            self.is_paused = True
            self.pause_event.clear()
            self.btn_pause.configure(text=i18n.t("btn_resume"), fg_color="#0284c7", hover_color="#0369a1")
            self.lbl_status.configure(text="⏸️ 下載已暫停，點擊「繼續下載」以恢復")
            self.log("⏸️ 使用者暫停了下載任務")
            for s in self.songs:
                if s.get('status') == 'downloading':
                    s['status'] = 'paused'
                    self._update_song_status(s, "⏸️ 已暫停", "#94a3b8")

    def cancel_download(self):
        """停止/取消當前下載任務（毫秒級即時響應，絕不卡死）"""
        if not self.is_running:
            return
        self.cancel_requested = True
        self.is_paused = False
        self.pause_event.set()

        self.btn_pause.configure(state="disabled", fg_color="#334155")
        self.btn_cancel.configure(state="disabled", fg_color="#334155", text="⏹️ 停止中...")
        self.lbl_status.configure(text="⏹️ 正在停止下載任務...")
        self.log("⏹️ 使用者已要求立即停止下載任務")

        for s in self.songs:
            if s.get('status') in ('downloading', 'paused', '等待中'):
                s['status'] = 'stopped'
                self._update_song_status(s, "⏹️ 已停止", "#64748b")

        if hasattr(self, '_current_executor') and self._current_executor:
            try:
                self._current_executor.shutdown(wait=False, cancel_futures=True)
            except Exception:
                pass

    def retry_failed_items(self):
        """重試所有失敗的項目"""
        failed = [s for s in self.songs if s.get('error')]
        if not failed:
            messagebox.showinfo("提示", "目前清單中沒有失敗的項目！")
            return

        for s in self.songs:
            if s in failed:
                s['var'].set(True)
                s['error'] = None
                self._update_song_status(s, "⏳ 等待重試", "#cbd5e1")
            else:
                s['var'].set(False)

        self.update_stats()
        self.log(f"🔄 準備重新嘗試下載 {len(failed)} 個失敗項目...")
        self.start_download_batch()

    def start_download_batch(self):
        if self.is_running:
            return

        selected_songs = [s for s in self.songs if s['var'].get()]
        if not selected_songs:
            messagebox.showwarning("提示", "清單中沒有勾選任何歌曲！請先加入歌曲並勾選。")
            return

        output_dir = self.entry_dir.get().strip()
        if not output_dir:
            messagebox.showwarning("提示", "請指定下載儲存目錄！")
            return

        # 下載前確保檢查資料夾編號格式
        use_numbering = bool(self.chk_numbering.get())
        if use_numbering:
            check_res = downloader.check_folder_numbering(output_dir)
            if check_res['status'] == 'not_numbered':
                self.inspect_folder_format(user_triggered=False)
                use_numbering = bool(self.chk_numbering.get())
            elif check_res['status'] == 'already_numbered':
                self.next_number = check_res['next_number']

        fmt_choice = self.opt_format.get()
        format_type = extract_format_code(fmt_choice)

        q_raw = self.opt_quality.get()
        if format_type in downloader.VIDEO_FORMATS:
            if "2160" in q_raw or "4k" in q_raw.lower():
                quality = "2160"
            elif "1440" in q_raw or "2k" in q_raw.lower():
                quality = "1440"
            elif "1080" in q_raw:
                quality = "1080"
            elif "720" in q_raw:
                quality = "720"
            elif "480" in q_raw:
                quality = "480"
            elif "360" in q_raw:
                quality = "360"
            else:
                quality = "best"
        elif format_type in ('wav', 'flac'):
            quality = "lossless"
        else:
            quality = q_raw.split()[0]

        embed_thumb = bool(self.chk_thumb.get()) and (format_type in ('mp3', 'm4a', 'flac', 'ogg'))
        embed_meta = bool(self.chk_meta.get())
        start_num = self.next_number if use_numbering else None

        self.is_running = True
        self.is_paused = False
        self.cancel_requested = False
        self.pause_event.set()
        self.duplicate_action_all = None
        self.failed_items = []

        # 切換三顆常駐按鈕狀態（主按鈕鎖定，暫停與停止亮起）
        self.btn_download.configure(state="disabled", fg_color="#1e293b", text="⚡ 下載任務進行中...")
        self.btn_pause.configure(state="normal", fg_color="#f59e0b", text=i18n.t("btn_pause"))
        self.btn_cancel.configure(state="normal", fg_color="#ef4444", text=i18n.t("btn_cancel"))
        self.btn_add.configure(state="disabled")

        max_workers = self.get_selected_thread_count()
        self.log(f"🎬 開始批次下載任務：共 {len(selected_songs)} 首，格式: {format_type.upper()}，音質/畫質: {quality}，併發線程: {max_workers}")

        threading.Thread(
            target=self._worker_download,
            args=(selected_songs, output_dir, format_type, quality, embed_thumb, embed_meta, start_num, max_workers),
            daemon=True
        ).start()

    def _worker_download(self, songs, output_dir, format_type, quality, embed_thumb, embed_meta, start_num, max_workers=3):
        total = len(songs)
        success_count = 0
        fail_count = 0
        skip_count = 0
        completed_count = 0
        prog_lock = threading.Lock()

        # 預先為每首歌曲分配前綴編號（若啟用 001 編號功能），保證多線程併發時檔名序號依然嚴格按照清單順序排列
        for idx, s in enumerate(songs):
            if start_num is not None:
                s['_assigned_num'] = start_num + idx
                s['_prefix_str'] = f"{s['_assigned_num']:03d} - "
            else:
                s['_assigned_num'] = None
                s['_prefix_str'] = ""

        def download_single_song(song_idx, song):
            nonlocal success_count, fail_count, skip_count, completed_count

            # 1. 檢查是否已取消
            if self.cancel_requested:
                return

            # 2. 檢查是否暫停中
            while not self.pause_event.is_set():
                if self.cancel_requested:
                    return
                time.sleep(0.2)

            if self.cancel_requested:
                return

            target_ext = f".{format_type}"
            safe_title = downloader.sanitize_filename(song['title'])
            prefix_str = song.get('_prefix_str', '')
            custom_stem = None
            overwrite_flag = True

            # 3. 查重防覆蓋處理（使用 Lock 保證只會跳出一個重複對話框）
            with self.duplicate_lock:
                if self.cancel_requested:
                    return
                dup = downloader.find_existing_duplicate(output_dir, song['title'], target_ext)
                if dup:
                    dup_filename, dup_path = dup
                    self.log(f"🔍 [查重發現] 資料夾已有相似檔案: {dup_filename}")
                    if self.duplicate_action_all:
                        action = self.duplicate_action_all
                    else:
                        action, apply_all = self.ask_duplicate_action(song['title'], dup_filename)
                        if apply_all:
                            self.duplicate_action_all = action

                    if action == "skip":
                        with prog_lock:
                            skip_count += 1
                            completed_count += 1
                            pct = completed_count / total
                            self.after(0, lambda p=pct: self.prog_bar.set(p))
                        self.log(f"⏭️ [略過] 略過重複歌曲: {song['title']}")
                        self.after(0, lambda s=song: self._update_song_status(s, "⏭️ 已略過", "#94a3b8"))
                        return

                    elif action == "suffix":
                        custom_stem, _ = downloader.get_unique_suffix_stem(output_dir, prefix_str, safe_title, target_ext)
                        self.log(f"➕ [後綴] 為避免衝突，產生新檔名: {custom_stem}{target_ext}")
                        overwrite_flag = False

                    else:
                        self.log(f"🔁 [覆蓋] 覆蓋舊檔: {dup_filename}")
                        overwrite_flag = True

            # 4. 開始執行下載
            display_name = f"{custom_stem}{target_ext}" if custom_stem else f"{prefix_str}{song['title']}"
            song['status'] = 'downloading'
            self.after(0, lambda s=song: self._update_song_status(s, "⚡ 下載中...", "#f59e0b"))
            self.log(f"📥 [{song_idx}/{total}] 啟動下載: {display_name}")

            last_song_hook = [0.0]
            def _song_hook(d):
                if self.is_paused or self.cancel_requested:
                    return
                now = time.time()
                if now - last_song_hook[0] < 0.3:
                    return
                last_song_hook[0] = now
                status = d.get('status')
                if status == 'downloading':
                    pct = d.get('_percent_str', '').strip()
                    if pct and song.get('status') == 'downloading':
                        self.after(0, lambda s=song, p=pct: self._update_song_status(s, f"⚡ 下載中 ({p})", "#f59e0b"))
                elif status == 'finished':
                    song['status'] = 'converting'
                    self.after(0, lambda s=song: self._update_song_status(s, "🔄 轉檔中...", "#38bdf8"))

            try:
                media_path = downloader.download_media(
                    url=song['url'],
                    output_dir=output_dir,
                    format_type=format_type,
                    quality=quality,
                    embed_thumbnail=embed_thumb,
                    embed_metadata=embed_meta,
                    progress_hook=_song_hook,
                    number_prefix=prefix_str if not custom_stem else None,
                    custom_filename=custom_stem,
                    overwrite=overwrite_flag,
                    log_callback=self.log,
                    cancel_check=lambda: self.cancel_requested,
                    pause_check=lambda: not self.pause_event.is_set()
                )
                song['file_path'] = media_path
                song['error'] = None
                song['status'] = 'completed'
                with prog_lock:
                    success_count += 1
                    completed_count += 1
                    pct = completed_count / total
                    self.after(0, lambda p=pct: self.prog_bar.set(p))
                    self.after(0, lambda c=completed_count, t=total: self.lbl_status.configure(text=f"📥 下載進度: [{c}/{t}] 首完成"))
                self.log(f"✅ 成功完成 [{song_idx}/{total}]: {os.path.basename(media_path)}")
                self.after(0, lambda s=song: self._update_song_status(s, "✅ 已完成", "#10b981"))

            except downloader.DownloadCancelled:
                with prog_lock:
                    completed_count += 1
                    pct = completed_count / total
                    self.after(0, lambda p=pct: self.prog_bar.set(p))
                song['status'] = 'stopped'
                self.after(0, lambda s=song: self._update_song_status(s, "⏹️ 已停止", "#64748b"))
                return

            except Exception as ex:
                with prog_lock:
                    completed_count += 1
                    pct = completed_count / total
                    self.after(0, lambda p=pct: self.prog_bar.set(p))
                if self.cancel_requested:
                    song['status'] = 'stopped'
                    self.after(0, lambda s=song: self._update_song_status(s, "⏹️ 已停止", "#64748b"))
                    return
                with prog_lock:
                    fail_count += 1
                full_err = str(ex)
                song['error'] = full_err
                song['status'] = 'failed'
                self.failed_items.append({'song': song, 'title': song['title'], 'url': song['url'], 'error': full_err})
                self.log(f"❌ 下載失敗 [{song_idx}/{total}]: {song['title']} | 原因: {full_err}")
                self.after(0, lambda s=song: self._update_song_status(s, "❌ 失敗 (點擊看原因)", "#ef4444", error_clickable=True))

        from concurrent.futures import ThreadPoolExecutor
        workers = max(1, min(max_workers, len(songs)))
        self.log(f"🚀 多線程併發引擎已啟用：同時執行線程 = {workers}，FFmpeg 全核心加速已就緒")

        executor = ThreadPoolExecutor(max_workers=workers)
        self._current_executor = executor
        try:
            futures = [executor.submit(download_single_song, i, song) for i, song in enumerate(songs, 1)]
            for future in futures:
                try:
                    future.result()
                except Exception:
                    pass
        finally:
            try:
                executor.shutdown(wait=False, cancel_futures=True)
            except Exception:
                pass
            self._current_executor = None

        if start_num is not None:
            self.next_number = start_num + len(songs)

        self.after(0, lambda: self._on_download_finished(success_count, skip_count, fail_count, output_dir, format_type))

    def _update_song_status(self, song, text, color, error_clickable=False):
        if 'status_lbl' in song and song['status_lbl'].winfo_exists():
            song['status_lbl'].configure(text=text, text_color=color)
            if error_clickable:
                song['status_lbl'].configure(cursor="hand2")
            else:
                song['status_lbl'].configure(cursor="")

    def _on_download_finished(self, success_count, skip_count, fail_count, output_dir, format_type):
        self.is_running = False
        self.is_paused = False

        # 恢復按鈕狀態（主按鈕恢復為可點擊，暫停與停止變為 disabled）
        fmt = extract_format_code(self.opt_format.get())
        pattern = i18n.t("btn_start_download_pattern")
        self.btn_download.configure(state="normal", fg_color="#10b981", text=pattern.format(fmt=fmt.upper()))
        self.btn_pause.configure(state="disabled", fg_color="#334155", text=i18n.t("btn_pause"))
        self.btn_cancel.configure(state="disabled", fg_color="#334155", text=i18n.t("btn_cancel"))
        self.btn_add.configure(state="normal")

        if self.cancel_requested:
            self.lbl_status.configure(text=f"⏹️ 任務已取消。成功: {success_count} 首，略過: {skip_count} 首，失敗: {fail_count} 首。")
            self.log(f"⏹️ 下載已取消。統計: 成功 {success_count} 首 | 略過 {skip_count} 首 | 失敗 {fail_count} 首")
        else:
            self.prog_bar.set(1.0)
            self.lbl_status.configure(text=f"🎉 任務完成！成功: {success_count} 首，略過: {skip_count} 首，失敗: {fail_count} 首。")
            self.log(f"🎉 任務執行結束！成功: {success_count} 首 | 略過: {skip_count} 首 | 失敗: {fail_count} 首")

        # 失敗重試按鈕更新
        if fail_count > 0:
            self.btn_retry_failed.configure(text=f"🔄 重試失敗 ({fail_count} 首)")
            self.btn_retry_failed.pack(side="right", padx=6)
        else:
            self.btn_retry_failed.pack_forget()

        # 刷新編號標籤提示
        if self.chk_numbering.get():
            self.lbl_num_info.configure(text=f"（已接續至 {self.next_number-1:03d}，下次將從 {self.next_number:03d} 開始）")

        # 若有失敗項目，彈出詳細失敗診斷報告與重試對話框
        if fail_count > 0:
            FailureReportDialog(self, self.failed_items, self.retry_failed_items)
        elif not self.cancel_requested:
            msg = (
                f"下載任務已全部完成！\n\n"
                f"格式: {format_type.upper()}\n"
                f"✅ 成功: {success_count} 個\n"
                f"⏭️ 略過: {skip_count} 個\n"
                f"❌ 失敗: {fail_count} 個\n\n"
                f"檔案已存於: {output_dir}\n"
                f"是否立即開啟下載資料夾？"
            )
            if messagebox.askyesno("下載完成", msg, parent=self):
                self.open_download_folder()


if __name__ == "__main__":
    app = MediaDownloaderApp()
    app.mainloop()
