# Changelog (版本更新紀錄)

All notable changes to the **StreamForge** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [v1.1.0] - 2026-09-30

### ✨ Added (全新功能)
- **🔌 Dynamic USB Hotplug Auto-Detection (USB 隨身碟動態熱插拔感應)**:
  - Hooks directly into Windows native `WM_DEVICECHANGE` (0x0219) message loop via ctypes/win32 window procedure.
  - Automatically updates the destination directory dropdown immediately upon USB device insertion or removal.
  - Displays instant non-intrusive notification with one-click button to set inserted USB drive as active download destination.
  - Safely falls back to default `Downloads` folder when an active USB drive is disconnected, preventing crashes or write errors.
- **📑 StreamForge Playlist Specification (`.sfpl` 歌單匯出與匯入)**:
  - Introduced custom, human-readable JSON-based playlist format (`.sfpl`) containing playlist metadata, song titles, original streaming URLs, and timestamps.
  - Added export and import dialogs allowing users to back up queues or share song lists.
  - Supported choice between "Overwriting existing queue" and "Appending to current queue".
  - Windows file type association registered in Inno Setup (`.sfpl` files receive custom application icon and launch StreamForge on double-click).
- **🚀 What's New & Changelog Tab in GUI (應用程式內版本更新紀錄)**:
  - Added dedicated "🚀 更新紀錄 / What's New" tab within the "About & License" dialog (`AboutDialog`).
  - Supports dynamic 8-language tab headers and formatted release notes.

### 🛠️ Fixed & Improved (問題修復與效能優化)
- **突破 YouTube 播放清單 100 首限制 (Playlist 100 Limit Removed)**:
  - Removed hardcoded `playlistend: 100` limit, allowing seamless analysis and retrieval of large playlists containing hundreds of tracks.
- **YouTube 403 Forbidden 指數退避自動重試 (Auto-Retry on 403 Forbidden)**:
  - Configured yt-dlp extractor retries and exponential backoff retry handler for streaming chunks.
  - Set `http_chunk_size` to 10MB to maintain smooth streaming data flow and prevent YouTube throttling.
- **清理殘留 `.webp` 縮圖與檔名重複編碼 (Clean Leftover Thumbnails & Fix Filename Growth)**:
  - Ensured temporary `.webp` thumbnails are immediately removed even when a download fails or is cancelled.
  - Eliminated repeated filename numbering and excessive encoding lengths.
- **清空清單與自動清理機制 (Instant Song List Clearing & Auto-Clean)**:
  - Fixed unresponsive "清空清單" button by switching to non-blocking UI queue clearing.
  - Automatically removes successfully completed songs upon batch completion to maintain a tidy interface.

### 📦 Installer & Safety (安裝程式與安全防護)
- **智慧平滑升級模式 (Smart Upgrade Mode)**:
  - Added semantic version comparison (`CompareVersion`) in Inno Setup installer.
  - Automatically recognizes version upgrades (e.g. `v1.0.0` -> `v1.1.0`), skips maintenance selection prompt, targets existing directory, and preserves user settings (`config.json`).
- **解除安裝前程式執行守護 (Uninstall Guard)**:
  - Installer/Uninstaller detects running `StreamForge.exe` and prompts user before termination.
  - If user declines termination, uninstallation is immediately aborted without deleting any files.

---

## [v1.0.0] - 2026-09-29

### ✨ Initial Release (首次正式發布)
- High-speed audio & video downloading engine powered by `yt-dlp` and `FFmpeg`.
- Built-in Format Factory converter supporting:
  - Audio: MP3, WAV, FLAC, M4A, AAC, OGG, OPUS (up to 320kbps / lossless).
  - Video: MP4, MKV, WEBM, MOV, AVI (up to 4K 60fps).
- Multi-core CPU parallel conversion and multi-threading download queue.
- Automatic metadata tagging (ID3v2.3) and high-resolution album cover embedding.
- Modern dark-themed GUI built with CustomTkinter.
- 8 international languages supported: Traditional Chinese, Simplified Chinese, English, Japanese, Korean, Spanish, French, German.
- Portable standalone executable and signed Windows Inno Setup installer.
