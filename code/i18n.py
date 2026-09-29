# -*- coding: utf-8 -*-
"""
StreamForge 多國語言模組 (Internationalization / i18n)
支援：繁體中文 (zh_TW)、English (en_US)、簡體中文 (zh_CN)、日本語 (ja_JP)
"""

LANGUAGES = {
    "zh_TW": "繁體中文",
    "en_US": "English",
    "zh_CN": "简体中文",
    "ja_JP": "日本語",
}

LANG_CODE_MAP = {
    "繁體中文": "zh_TW",
    "English": "en_US",
    "简体中文": "zh_CN",
    "日本語": "ja_JP",
}

_CURRENT_LANG = "zh_TW"

STRINGS = {
    # 標題與標語
    "app_title": {
        "zh_TW": "⚡ StreamForge · 串流影音工坊 (MP3 / MP4 · 命令終端版)",
        "en_US": "⚡ StreamForge · Media Stream Studio (MP3 / MP4 · CLI Edition)",
        "zh_CN": "⚡ StreamForge · 流媒体影音工坊 (MP3 / MP4 · 命令终端版)",
        "ja_JP": "⚡ StreamForge · ストリーミングメディア工房 (MP3 / MP4 · コマンド版)",
    },
    "app_subtitle": {
        "zh_TW": "逐條加入 · 暫停/取消控制 · 資料夾查重防覆蓋 · 隨身碟 001 編號智慧檢查 · 即時命令列狀態 · 失敗詳細報告與重試",
        "en_US": "Batch Queue · Pause/Cancel · Conflict Prevention · USB 001 Numbering · Live Terminal · Error Diagnostics & Retry",
        "zh_CN": "逐条添加 · 暂停/取消控制 · 文件夹查重防覆盖 · U盘 001 编号智能检查 · 实时命令行状态 · 失败详细报告与重试",
        "ja_JP": "個別追加 · 一時停止/中止 · 重複防止 · USB 001 連番検査 · インタラクティブ CLI · エラー報告と再試行",
    },
    "btn_about": {
        "zh_TW": "ℹ️ 關於 / 授權",
        "en_US": "ℹ️ About / License",
        "zh_CN": "ℹ️ 关于 / 授权",
        "ja_JP": "ℹ️ 情報 / ライセンス",
    },
    # 區塊 1: 新增歌曲
    "sec_add_song": {
        "zh_TW": "🎵 1. 新增下載歌曲 (支援單曲與播放清單網址)",
        "en_US": "🎵 1. Add Media Links (Supports Single Tracks & Playlists)",
        "zh_CN": "🎵 1. 添加下载歌曲 (支持单曲与播放列表网址)",
        "ja_JP": "🎵 1. メディア追加 (単曲およびプレイリストURL対応)",
    },
    "url_placeholder": {
        "zh_TW": "請在此貼上串流影片/音訊網址 (支援 YouTube、bilibili、SoundCloud...)",
        "en_US": "Paste video/audio URL here (YouTube, bilibili, SoundCloud...)",
        "zh_CN": "请在此粘贴视频/音频网址 (支持 YouTube、bilibili、SoundCloud...)",
        "ja_JP": "動画・音声URLをここに貼り付け (YouTube、bilibili、SoundCloudなど)",
    },
    "btn_paste": {
        "zh_TW": "📋 貼上",
        "en_US": "📋 Paste",
        "zh_CN": "📋 粘贴",
        "ja_JP": "📋 貼付",
    },
    "btn_add": {
        "zh_TW": "➕ 加入清單",
        "en_US": "➕ Add to Queue",
        "zh_CN": "➕ 加入列表",
        "ja_JP": "➕ キューに追加",
    },
    # 區塊 2: 儲存目錄與設定
    "sec_download_settings": {
        "zh_TW": "📁 2. 儲存目錄與下載設定",
        "en_US": "📁 2. Save Directory & Download Settings",
        "zh_CN": "📁 2. 保存目录与下载设置",
        "ja_JP": "📁 2. 保存先フォルダとダウンロード設定",
    },
    "lbl_save_dir": {
        "zh_TW": "儲存資料夾：",
        "en_US": "Save Folder:",
        "zh_CN": "保存文件夹：",
        "ja_JP": "保存先：",
    },
    "btn_browse": {
        "zh_TW": "瀏覽...",
        "en_US": "Browse...",
        "zh_CN": "浏览...",
        "ja_JP": "参照...",
    },
    "btn_open_folder": {
        "zh_TW": "開啟資料夾",
        "en_US": "Open Folder",
        "zh_CN": "打开文件夹",
        "ja_JP": "開く",
    },
    "btn_check_format": {
        "zh_TW": "🔍 檢查資料夾編號格式",
        "en_US": "🔍 Inspect Numbering Format",
        "zh_CN": "🔍 检查文件夹编号格式",
        "ja_JP": "🔍 連番フォーマット検査",
    },
    "lbl_format": {
        "zh_TW": "下載格式：",
        "en_US": "Format:",
        "zh_CN": "下载格式：",
        "ja_JP": "ダウンロード形式：",
    },
    "lbl_quality": {
        "zh_TW": "音質/畫質：",
        "en_US": "Quality:",
        "zh_CN": "音质/画质：",
        "ja_JP": "品質：",
    },
    "chk_auto_number": {
        "zh_TW": "檔名前加入 001/002 序號",
        "en_US": "Add 001, 002 prefix to filename",
        "zh_CN": "文件名前加入 001/002 序号",
        "ja_JP": "ファイル名に 001 連番を付加",
    },
    # 區塊 3: 清單管理
    "sec_queue_list": {
        "zh_TW": "📋 3. 下載清單",
        "en_US": "📋 3. Download Queue",
        "zh_CN": "📋 3. 下载列表",
        "ja_JP": "📋 3. ダウンロードキュー",
    },
    "btn_select_all": {
        "zh_TW": "全選",
        "en_US": "Select All",
        "zh_CN": "全选",
        "ja_JP": "全選択",
    },
    "btn_deselect_all": {
        "zh_TW": "取消全選",
        "en_US": "Deselect All",
        "zh_CN": "全不选",
        "ja_JP": "全解除",
    },
    "btn_clear_list": {
        "zh_TW": "清空已完成",
        "en_US": "Clear Completed",
        "zh_CN": "清除已完成",
        "ja_JP": "完了をクリア",
    },
    "btn_start_download": {
        "zh_TW": "🚀 開始下載",
        "en_US": "🚀 Start Download",
        "zh_CN": "🚀 开始下载",
        "ja_JP": "🚀 ダウンロード開始",
    },
    "btn_pause": {
        "zh_TW": "⏸️ 暫停",
        "en_US": "⏸️ Pause",
        "zh_CN": "⏸️ 暂停",
        "ja_JP": "⏸️ 一時停止",
    },
    "btn_resume": {
        "zh_TW": "▶️ 繼續",
        "en_US": "▶️ Resume",
        "zh_CN": "▶️ 继续",
        "ja_JP": "▶️ 再開",
    },
    "btn_cancel": {
        "zh_TW": "⏹️ 取消任務",
        "en_US": "⏹️ Cancel",
        "zh_CN": "⏹️ 取消任务",
        "ja_JP": "⏹️ 中止",
    },
    "btn_retry_failed": {
        "zh_TW": "🔄 重試失敗項目",
        "en_US": "🔄 Retry Failed",
        "zh_CN": "🔄 重试失败项",
        "ja_JP": "🔄 失敗を再試行",
    },
    # 區塊 4: 終端機控制台
    "sec_cmd_console": {
        "zh_TW": "💻 即時命令列狀態 (Terminal Prompt)",
        "en_US": "💻 Interactive Terminal & Status",
        "zh_CN": "💻 实时命令行状态 (Terminal Prompt)",
        "ja_JP": "💻 インタラクティブターミナル (Terminal Prompt)",
    },
    "btn_clear_log": {
        "zh_TW": "清除畫面",
        "en_US": "Clear Output",
        "zh_CN": "清除屏幕",
        "ja_JP": "クリア",
    },
    "cmd_placeholder": {
        "zh_TW": "輸入指令... (例如: help, add <網址>, list, start, pause, resume, cancel, retry, update)",
        "en_US": "Enter command... (e.g. help, add <url>, list, start, pause, resume, cancel, retry, update)",
        "zh_CN": "输入指令... (例如: help, add <网址>, list, start, pause, resume, cancel, retry, update)",
        "ja_JP": "コマンド入力... (例: help, add <URL>, list, start, pause, resume, cancel, retry, update)",
    },
    "btn_send_cmd": {
        "zh_TW": "送出 (Enter)",
        "en_US": "Send (Enter)",
        "zh_CN": "发送 (Enter)",
        "ja_JP": "送信 (Enter)",
    },
    # 關於我們對話框
    "about_title": {
        "zh_TW": "ℹ️ 關於 StreamForge · 智慧財產權與免責聲明",
        "en_US": "ℹ️ About StreamForge · Intellectual Property & Disclaimer",
        "zh_CN": "ℹ️ 关于 StreamForge · 知识产权与免责声明",
        "ja_JP": "ℹ️ StreamForge について · 知的財産権と免責事項",
    },
    "tab_about": {
        "zh_TW": "🏢 關於我們",
        "en_US": "🏢 About Us",
        "zh_CN": "🏢 关于我们",
        "ja_JP": "🏢 概要",
    },
    "tab_disclaimer": {
        "zh_TW": "⚖️ 法律免責聲明",
        "en_US": "⚖️ Legal Disclaimer",
        "zh_CN": "⚖️ 法律免责声明",
        "ja_JP": "⚖️ 免責事項",
    },
    "tab_license": {
        "zh_TW": "📜 授權合約 (MIT)",
        "en_US": "📜 License (MIT)",
        "zh_CN": "📜 授权协议 (MIT)",
        "ja_JP": "📜 ライセンス (MIT)",
    },
    "product_name_lbl": {
        "zh_TW": "🏷️ 產品名稱",
        "en_US": "🏷️ Product Name",
        "zh_CN": "🏷️ 产品名称",
        "ja_JP": "🏷️ 製品名",
    },
    "install_date_lbl": {
        "zh_TW": "📅 安裝日期",
        "en_US": "📅 Install Date",
        "zh_CN": "📅 安装日期",
        "ja_JP": "📅 インストール日",
    },
    "dev_team_lbl": {
        "zh_TW": "👥 開發團隊",
        "en_US": "👥 Developer Team",
        "zh_CN": "👥 开发团队",
        "ja_JP": "👥 開発チーム",
    },
    "license_lbl": {
        "zh_TW": "📜 軟體授權",
        "en_US": "📜 License",
        "zh_CN": "📜 软件授权",
        "ja_JP": "📜 ライセンス",
    },
    "copyright_lbl": {
        "zh_TW": "© 智慧財產權",
        "en_US": "© Copyright",
        "zh_CN": "© 知识产权",
        "ja_JP": "© 著作権",
    },
    "project_home_lbl": {
        "zh_TW": "🌐 官方專案",
        "en_US": "🌐 GitHub Repo",
        "zh_CN": "🌐 官方项目",
        "ja_JP": "🌐 プロジェクト",
    },
    "chk_autoupdate": {
        "zh_TW": "☑️ 啟動應用程式時自動檢查最新發布版本 (Auto-check updates)",
        "en_US": "☑️ Automatically check for updates on startup",
        "zh_CN": "☑️ 启动应用程序时自动检查最新发布版本 (Auto-check updates)",
        "ja_JP": "☑️ 起動時に最新バージョンの更新を自動確認する",
    },
    "btn_check_now": {
        "zh_TW": "🔄 立即檢查更新",
        "en_US": "🔄 Check Updates Now",
        "zh_CN": "🔄 立即检查更新",
        "ja_JP": "🔄 今すぐ更新確認",
    },
    "btn_open_repo": {
        "zh_TW": "🌐 前往 Releases 頁面",
        "en_US": "🌐 Visit Releases Page",
        "zh_CN": "🌐 前往 Releases 页面",
        "ja_JP": "🌐 リリース一覧へ",
    },
    "btn_copy_disclaimer": {
        "zh_TW": "📋 複製免責與版權宣告",
        "en_US": "📋 Copy Disclaimer & Copyright",
        "zh_CN": "📋 复制免责与版权宣告",
        "ja_JP": "📋 免責条項と著作権をコピー",
    },
    "btn_close": {
        "zh_TW": "關閉",
        "en_US": "Close",
        "zh_CN": "关闭",
        "ja_JP": "閉じる",
    },
    "lang_selector_label": {
        "zh_TW": "🌐 介面語言 / Language：",
        "en_US": "🌐 Display Language:",
        "zh_CN": "🌐 界面语言 / Language：",
        "ja_JP": "🌐 表示言語 / Language：",
    },
    "btn_sample": {
        "zh_TW": "✨ 測試範例",
        "en_US": "✨ Sample Link",
        "zh_CN": "✨ 测试示例",
        "ja_JP": "✨ サンプル",
    },
    "btn_usb": {
        "zh_TW": "💾 隨身碟",
        "en_US": "💾 USB Drive",
        "zh_CN": "💾 U盘",
        "ja_JP": "💾 USBメモリ",
    },
    "chk_thumb": {
        "zh_TW": "🖼️ 嵌入封面縮圖",
        "en_US": "🖼️ Embed Thumbnail",
        "zh_CN": "🖼️ 嵌入封面缩略图",
        "ja_JP": "🖼️ アートワーク埋込",
    },
    "chk_meta": {
        "zh_TW": "🏷️ 嵌入標籤資訊",
        "en_US": "🏷️ Embed Metadata",
        "zh_CN": "🏷️ 嵌入标签信息",
        "ja_JP": "🏷️ メタデータ埋込",
    },
    "lbl_quality_audio": {
        "zh_TW": "🎧 音質位元率:",
        "en_US": "🎧 Audio Bitrate:",
        "zh_CN": "🎧 音质比特率:",
        "ja_JP": "🎧 音質ビットレート:",
    },
    "lbl_quality_video": {
        "zh_TW": "📺 影片解析度:",
        "en_US": "📺 Video Resolution:",
        "zh_CN": "📺 视频分辨率:",
        "ja_JP": "📺 動画解像度:",
    },
    "lbl_empty_list": {
        "zh_TW": "清單目前是空的。\n請在上方貼上網址並點擊「➕ 加入清單」，一條一條累積您的下載清單！",
        "en_US": "The download queue is currently empty.\nPaste a URL above and click '➕ Add to Queue' to build your list!",
        "zh_CN": "列表目前是空的。\n请在上方粘贴网址并点击“➕ 加入列表”，一条一条积累您的下载列表！",
        "ja_JP": "キューは現在空です。\n上記にURLを貼り付けて「➕ キューに追加」をクリックしてください。",
    },
    "btn_start_download_mp3": {
        "zh_TW": "🚀 一次下載清單中所有選取的項目 (轉為 MP3)",
        "en_US": "🚀 Download All Selected Items (Convert to MP3)",
        "zh_CN": "🚀 一次下载列表中所有选中的项目 (转为 MP3)",
        "ja_JP": "🚀 選択した項目を一括ダウンロード (MP3に変換)",
    },
    "btn_start_download_mp4": {
        "zh_TW": "🚀 一次下載清單中所有選取的項目 (轉為 MP4 影片)",
        "en_US": "🚀 Download All Selected Items (Convert to MP4 Video)",
        "zh_CN": "🚀 一次下载列表中所有选中的项目 (转为 MP4 视频)",
        "ja_JP": "🚀 選択した項目を一括ダウンロード (MP4動画に変換)",
    },
    "stats_pattern": {
        "zh_TW": "📊 待下載清單 (共 {total} 首 | 已選 {selected} 首)",
        "en_US": "📊 Download Queue ({total} items | {selected} selected)",
        "zh_CN": "📊 待下载列表 (共 {total} 首 | 已选 {selected} 首)",
        "ja_JP": "📊 ダウンロードキュー (全 {total} 件 | 選択中 {selected} 件)",
    },
    "status_ready": {
        "zh_TW": "系統就緒，等待加入網址",
        "en_US": "Ready, waiting for URLs to be added",
        "zh_CN": "系统就绪，等待加入网址",
        "ja_JP": "準備完了、URLの追加を待機中",
    },
    "lang_switched": {
        "zh_TW": "已切換介面語言為",
        "en_US": "Interface language switched to",
        "zh_CN": "已切换界面语言为",
        "ja_JP": "表示言語を切り替えました：",
    },
    "btn_expand": {
        "zh_TW": "展開 ▼",
        "en_US": "Expand ▼",
        "zh_CN": "展开 ▼",
        "ja_JP": "展開 ▼",
    },
    "btn_collapse": {
        "zh_TW": "收合 ▲",
        "en_US": "Collapse ▲",
        "zh_CN": "收起 ▲",
        "ja_JP": "格納 ▲",
    },
}


def get_current_language() -> str:
    """取得當前語言代碼 (預設 zh_TW)"""
    global _CURRENT_LANG
    return _CURRENT_LANG


def set_current_language(lang_code: str):
    """設定當前語言代碼"""
    global _CURRENT_LANG
    if lang_code in LANGUAGES:
        _CURRENT_LANG = lang_code
    elif lang_code in LANG_CODE_MAP:
        _CURRENT_LANG = LANG_CODE_MAP[lang_code]


def t(key: str, default: str = None) -> str:
    """取得指定 key 的多國語言字串"""
    lang = get_current_language()
    item = STRINGS.get(key)
    if isinstance(item, dict):
        return item.get(lang, item.get("zh_TW", default or key))
    return default or key
