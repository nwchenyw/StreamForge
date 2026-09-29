<div align="center">

# ⚡ StreamForge
### 高性能串流影音工坊 · 跨格式轉換與智慧檔名管理工具
**High-Performance Media Stream & Audio Processing Utility**

<p align="center">
  <a href="README.md"><b>繁體中文 (預設)</b></a> •
  <a href="README.en.md"><b>English</b></a> •
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
  <b>支援 8 國語言即時切換 · MP3 / MP4 切換 · 隨身碟智慧辨識 · 001 循序編號 · 目標目錄防覆蓋查重 · 失敗診斷與一鍵重試 · 內建交互式命令列 (CLI)</b>
</p>

</div>

---

## 🌟 核心特色 (Key Features)

- 🌐 **多國語言介面 (8 國語言支援)**：
  - 支援 **繁體中文、English、简体中文、日本語、한국어、Español、Français、Deutsch**。
  - **安裝精靈支援多語言**：啟動安裝檔時即可選擇語言。
  - **應用程式內隨時切換**：在主視窗右上角或「關於 / 授權」對話框皆可一鍵切換，介面文字即時更新，無須重啟。
- 🎵 **多格式彈性切換**：
  - **MP3 純音訊**：最高 320 kbps 高音質轉檔，自動寫入 ID3 歌曲標籤與嵌入專輯封面。
  - **🎬 MP4 視訊影片**：支援最高畫質（1080p Full HD / 720p HD 等），自動合併高畫質視訊與音訊。
- 💾 **USB 隨身碟與資料夾智慧檢查 (001, 002...)**：
  - 一鍵自動偵測插入的 USB 隨身碟。
  - 智慧檢查現有檔案編號格式，新檔案自動接續編號（如從 `016` 繼續）。
  - 若檔案未編號，主動詢問是否自動二階段重命名為 `001 - 檔名`（適合車載音響或播放器）。
- 🔍 **下載前目錄智慧查重**：
  - 下載前自動掃描目標資料夾，發現同名或相同歌曲時彈窗提供 **覆蓋**、**加上編號後綴 (1)** 或 **略過**，並支援「套用到全部」。
- ❌ **失敗詳細診斷與一鍵重試**：
  - 自動捕捉並分析每首歌曲失敗原因（如私人影片、平台驗證、HTTP 403 限速或網路逾時）。
  - 一鍵重試所有失敗項目，無需手動重新勾選。
- 💻 **交互式命令列控制台 (Interactive CLI Prompt)**：
  - 專為極客與進階玩家打造的終端操作面板，支援快速指令輸入、執行日誌串流與 `↑` / `↓` 歷史命令切換。
- 🛡️ **反爬蟲強化與長連線機制**：
  - 內建多平台客戶端模擬機制，大幅降低伺服器驗證失敗率，內建 10 次自動重試。

---

## 🎮 控制台指令一覽表 (CLI Commands)

您可以在工具下方的 **`💻 即時命令列狀態`** 輸入指令，完全使用鍵盤進行控制：

| 指令 | 簡稱/別名 | 功能說明與範例 |
| :--- | :--- | :--- |
| **`about`** | `copyright`, `team` | 顯示 StreamForge 軟體版本與智慧財產權宣告 |
| **`help`** | `?`, `h` | 顯示所有可用指令與說明 |
| **`add <網址>`** | `a <網址>` | 新增單曲或播放清單網址至清單中（例如：`add https://...`） |
| **`paste`** | `p` | 自動讀取系統剪貼簿中的網址並加入 |
| **`list`** | `ls` | 列出目前清單中所有歌曲、時長、勾選與下載狀態 |
| **`select <範圍>`** | `sel` | 選取歌曲：`select all`、`select none`、`select 1 3 5`、`select 1-5` |
| **`del <範圍>`** | `rm` | 刪除歌曲：`del 2`、`del 1 3`、`del all` |
| **`start`** | `dl`, `run` | 啟動批次下載所有已勾選的歌曲 |
| **`pause`** | - | 暫停當前下載任務 |
| **`resume`** | - | 恢復已暫停的下載任務 |
| **`cancel`** | `stop` | 取消當前下載任務（保留已完成檔案） |
| **`retry`** | `r` | 重新嘗試下載所有標記為失敗的歌曲 |
| **`format <格式>`** | `fmt` | 切換格式：`format mp3` 或 `format mp4` |
| **`quality <值>`** | `q` | 設定品質：音質 `quality 320` 或畫質 `quality 1080`、`quality best` |
| **`dir [路徑]`** | `cd` | 查看或切換下載儲存路徑，例如：`dir D:\MyMusic` |
| **`usb`** | - | 自動辨識插上的 USB 隨身碟並切換下載目錄 |
| **`check`** | - | 檢查目標資料夾是否符合 001 編號格式 |
| **`number <on/off>`**| `num` | 開啟或關閉檔名 001 前綴序號功能 |
| **`open`** | - | 在檔案總管開啟當前下載儲存資料夾 |
| **`status`** | - | 顯示目前系統設定、清單與下載狀態摘要 |
| **`clear`** | `cls` | 清除命令列控制台輸出畫面 |
| **`exit`** | `quit` | 關閉應用程式 |

---

## 🚀 下載與安裝 (Installation & Releases)

### 1. Windows 原生多國語言安裝精靈 (推薦)
前往 [Releases 頁面](https://github.com/nwchenyw/StreamForge/releases) 下載最新版的 **`StreamForge-Setup-v1.0.0.exe`**：
- **8 國語言安裝精靈**：啟動安裝時即可自由選擇偏好語言。
- **自選安裝位置**：可自由安裝於預設系統路徑、任意硬碟目錄或隨身碟。
- **捷徑設定**：安裝時可自由勾選是否建立桌面捷徑與開始功能表捷徑。
- **自動更新檢查**：安裝時與 App 內皆可勾選「啟動時自動檢查最新版本」。
- **純淨無腳本**：標準 Windows 原生安裝精靈，包含乾淨的解除安裝程式（可在「設定 > 應用程式」一鍵移除）。

### 2. 從原始碼執行 (開發者模式)
```bash
# 複製儲存庫
git clone https://github.com/nwchenyw/StreamForge.git
cd StreamForge

# 安裝依賴套件
pip install -r code/requirements.txt

# 啟動應用程式
python code/gui_app.py
```

### 3. 自行編譯 Windows 安裝程式
```bash
# 步驟 1: 生成執行目錄
python -m PyInstaller --onedir --noconsole --name "StreamForge" --collect-all customtkinter --add-data "code/ffmpeg_bin;ffmpeg_bin" code/gui_app.py --clean -y

# 步驟 2: 編譯 Inno Setup 多語言安裝檔
iscc .github/installer/installer.iss
# 產出檔案位於 installer/StreamForge-Setup-v1.0.0.exe
```

---

## ⚖️ 智慧財產權與法律免責聲明 (Legal Disclaimer)

### 版權宣告 (Copyright Notice)
**© 2026 The StreamForge Team & Contributors. All Rights Reserved.**  
本專案採用 **[MIT License](LICENSE)** 授權開源。

### 免責聲明 (Disclaimer)
1. 本專案為開源軟體，開發目的僅供**個人學習、研究、合理使用 (Fair Use) 以及備份個人合法內容**。
2. 本專案**不提供、不儲存、亦不分發**任何受著作權保護之媒體內容，所有下載數據均由使用者所提供之網路位址即時串流處理。
3. 使用者在使用本工具時，應自覺遵守所在國家/地區之智慧財產權法規及各影音平台之使用者服務條款。
4. 任何因不當使用、商業營利或侵犯他人智慧財產權所衍生之法律責任，均由使用者自行承擔，開發團隊不負任何連帶保證或法律責任。
