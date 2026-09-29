<div align="center">

# ⚡ StreamForge
### High-Performance Media Stream & Audio Processing Utility
**Cross-Format Conversion · Smart Numbering · Conflict Resolution · Interactive CLI**

<p align="center">
  <a href="README.zh-TW.md"><b>繁體中文</b></a> •
  <a href="README.md"><b>English</b></a> •
  <a href="README.zh-CN.md"><b>简体中文</b></a> •
  <a href="README.ja.md"><b>日本語</b></a> •
  <a href="README.ko.md"><b>한국어</b></a> •
  <a href="README.es.md"><b>Español</b></a> •
  <a href="README.fr.md"><b>Français</b></a> •
  <a href="README.de.md"><b>Deutsch</b></a>
</p>

[![Release](https://img.shields.io/badge/Release-v1.0.0-38bdf8?style=for-the-badge&logo=github)](https://github.com/nwchenyw/StreamForge/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-0284c7?style=for-the-badge&logo=windows)](https://microsoft.com)
[![Python](https://img.shields.io/badge/Python-3.12%2B-f59e0b?style=for-the-badge&logo=python)](https://python.org)
[![i18n](https://img.shields.io/badge/Languages-8%20Supported-purple?style=for-the-badge)](code/i18n.py)

<p align="center">
  <b>Supports 8 Languages · Seamless MP3 / MP4 Switching · USB Auto-Detection · 001 Numbering · Conflict Prevention · Error Diagnostics · Built-in CLI</b>
</p>

</div>

---

## 🌟 Key Features

- 🌐 **Comprehensive Multi-Language Support (8 Languages)**:
  - Full interface translation for **English, Traditional Chinese, Simplified Chinese, Japanese, Korean, Spanish, French, and German**.
  - **Installer Language Selector**: Choose your language directly in the setup wizard.
  - **In-App Dynamic Switcher**: Switch anytime from the top-right menu or the About dialog without restarting.
- 🎵 **Flexible Multi-Format Conversion**:
  - **MP3 Audio**: Up to 320 kbps high-bitrate conversion, automatic ID3 tag writing, and album artwork embedding.
  - **🎬 MP4 Video**: Supports up to Full HD 1080p and 720p HD with automated video/audio muxing.
- 💾 **Smart USB Drive & Folder Numbering (001, 002...)**:
  - One-click automatic detection of inserted USB drives.
  - Inspects existing files to automatically continue numbering sequences (e.g., resumes at `016`).
  - Offers smart two-phase batch renaming to `001 - Title` for automotive audio systems and media players.
- 🔍 **Pre-Download Duplicate Conflict Resolution**:
  - Automatically scans target directories before downloading. If matching files exist, provides **Overwrite**, **Append index (1)**, or **Skip** with an "Apply to All" option.
- ❌ **Detailed Error Diagnostics & One-Click Retry**:
  - Catches and categorizes failures (private videos, platform bot checks, HTTP 403 throttling, timeouts).
  - One-click retry for all failed tasks without re-adding links.
- 💻 **Interactive CLI Terminal**:
  - Built-in command prompt supporting keyboard navigation, streaming logs, and `↑` / `↓` command history.
- 🛡️ **Anti-Bot Simulation & Robust Connectivity**:
  - Emulates mobile APIs to drastically reduce server verification blocks, backed by automated retry loops.

---

## 🎮 CLI Commands Reference

You can control StreamForge completely via keyboard in the **`💻 Interactive Terminal`** at the bottom of the window:

| Command | Aliases | Description & Examples |
| :--- | :--- | :--- |
| **`about`** | `copyright`, `team` | Display version, developers, and copyright disclaimer |
| **`help`** | `?`, `h` | Show all available commands and syntax |
| **`add <url>`** | `a <url>` | Add a single video/audio track or playlist to queue |
| **`paste`** | `p` | Automatically read URL from system clipboard and add to queue |
| **`list`** | `ls` | List all queue items, duration, and download statuses |
| **`select <range>`** | `sel` | Select items: `select all`, `select none`, `select 1 3 5`, `select 1-5` |
| **`del <range>`** | `rm` | Remove items: `del 2`, `del 1 3`, `del all` |
| **`start`** | `dl`, `run` | Start downloading all selected items |
| **`pause`** | - | Pause active downloads |
| **`resume`** | - | Resume paused downloads |
| **`cancel`** | `stop` | Cancel active downloads (retains completed files) |
| **`retry`** | `r` | Retry all failed items in the queue |
| **`format <fmt>`** | `fmt` | Switch format: `format mp3` or `format mp4` |
| **`quality <val>`** | `q` | Set quality: `quality 320` or video `quality 1080`, `quality best` |
| **`dir [path]`** | `cd` | View or change destination folder, e.g.: `dir D:\Music` |
| **`usb`** | - | Automatically detect USB drive and switch download directory |
| **`check`** | - | Inspect whether destination folder conforms to 001 numbering |
| **`number <on/off>`**| `num` | Enable or disable filename 001 prefix sequencing |
| **`open`** | - | Open the current download folder in Windows File Explorer |
| **`status`** | - | Show system configuration and queue summary |
| **`clear`** | `cls` | Clear terminal console output |
| **`exit`** | `quit` | Exit application |

---

## 🚀 Installation & Releases

### 1. Windows Native Installer (Recommended)
Download the latest **`StreamForge-Setup-v1.0.0.exe`** from the [GitHub Releases](https://github.com/nwchenyw/StreamForge/releases) page:
- **8-Language Setup Wizard**: Select your preferred language right at launch.
- **Custom Destination**: Install to default Program Files, any secondary drive, or directly to a portable USB drive.
- **Shortcut Configuration**: Optional Desktop and Start Menu shortcuts.
- **Automatic Updates**: Enable startup update check during installation or later in settings.
- **Clean & Scriptless**: Standard Windows native installer with a clean uninstaller accessible via Windows Settings.

### 2. Run from Source (Developer Mode)
```bash
# Clone the repository
git clone https://github.com/nwchenyw/StreamForge.git
cd StreamForge

# Install dependencies
pip install -r code/requirements.txt

# Launch application
python code/gui_app.py
```

### 3. Build Windows Installer Locally
```bash
# Step 1: Package application
python -m PyInstaller --onedir --noconsole --name "StreamForge" --collect-all customtkinter --add-data "code/ffmpeg_bin;ffmpeg_bin" code/gui_app.py --clean -y

# Step 2: Compile Inno Setup installer
iscc .github/installer/installer.iss
# Output is saved to installer/StreamForge-Setup-v1.0.0.exe
```

---

## ⚖️ Intellectual Property & Legal Disclaimer

### Copyright Notice
**© 2026 The StreamForge Team & Contributors. All Rights Reserved.**  
This project is licensed under the **[MIT License](LICENSE)**.

### Disclaimer
1. This tool is open-source software intended strictly for **personal learning, research, fair use, and personal authorized backups**.
2. StreamForge **does not host, store, cache, or distribute** copyrighted media. All media streams are processed locally and directly from URLs provided by the user.
3. Users are responsible for complying with applicable copyright laws and streaming service Terms of Service in their jurisdiction.
4. The developers assume no liability for misuse, commercial redistribution, or copyright infringement.
