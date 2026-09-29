# 🎵 串流影音批次下載工具 (MP3 / MP4 · 命令終端版) - 原始碼說明

此資料夾存放本專案的所有原始碼、FFmpeg 依賴檔及設定檔。

---

## 📂 檔案清單說明

- **[`downloader.py`](file:///D:/Windows路徑用/桌面/MP3%20Downloader/code/downloader.py)**：核心下載、轉檔、查重與編號模組。
  - 封裝串流提取與多平台模擬（iOS / Android / 手機 Web），大幅降低伺服器機器人驗證失敗率。
  - 支援 MP3 最高 320kbps 音訊轉檔、ID3 標籤寫入與縮圖封面嵌入。
  - 支援 MP4 最高畫質 (1080p/720p/480p) 高畫質視訊與音訊自動合併。
  - Windows USB 隨身碟自動辨識與 001/002 格式檢查與二階段批次重命名。
  - 目標資料夾預先查重與衝突自動後綴 (1), (2) 生成。
  - 支援下載中取消檢查與即時 Logger 攔截。
- **[`gui_app.py`](file:///D:/Windows路徑用/桌面/MP3%20Downloader/code/gui_app.py)**：原生桌面 GUI 應用程式（使用 CustomTkinter）：
  - 💻 **交互式命令列控制台 (Interactive CLI Prompt)**：支援玩家輸入指令直接控制下載器，具備 `↑` / `↓` 歷史命令切換。
  - 逐條輸入與即時解析加入清單。
  - ⏸️ 暫停下載 / ▶️ 繼續下載 / ⏹️ 取消下載控制。
  - ⚠️ 重複檔案彈跳互動視窗（覆蓋 / 加上後綴(1) / 略過 / 套用到後續所有重複檔案）。
  - ❌ 失敗曲目詳細原因報告與一鍵重試失敗項目。
  - 隨身碟與自選資料夾 001 編號智慧檢查與自動接續。
- **[`ffmpeg_bin/`](file:///D:/Windows路徑用/桌面/MP3%20Downloader/code/ffmpeg_bin/)**：內建的完整 FFmpeg 8.0.1 與 FFprobe 執行檔。
- **[`requirements.txt`](file:///D:/Windows路徑用/桌面/MP3%20Downloader/code/requirements.txt)**：Python 依賴套件清單。

---

## 💻 控制台可用指令一覽表 (CLI Commands)

| 指令 | 別名 | 說明與範例 |
| :--- | :--- | :--- |
| `help` | `?`, `h` | 顯示所有可用指令與說明 |
| `add <網址>` | `a <網址>` | 新增歌曲或播放清單網址至清單中 |
| `paste` | `p` | 自動讀取系統剪貼簿中的網址並加入 |
| `list` | `ls` | 列出目前清單中所有歌曲、時長、勾選與下載狀態 |
| `select <範圍>` | `sel` | 選取或反選。例如：`select all`、`select none`、`select 1 3 5`、`select 1-5` |
| `del <範圍>` | `rm` | 刪除歌曲。例如：`del 2`、`del 1 3`、`del all` |
| `start` | `dl`, `run` | 啟動批次下載所有已勾選的歌曲 |
| `pause` | - | 暫停當前下載任務 |
| `resume` | - | 恢復已暫停的下載任務 |
| `cancel` | `stop` | 取消當前下載任務（保留已完成的檔案） |
| `retry` | `r` | 重新下載所有標記為失敗的歌曲 |
| `format <格式>` | `fmt` | 切換格式：`format mp3` 或 `format mp4` |
| `quality <值>` | `q` | 設定品質：音質 `quality 320` 或畫質 `quality 1080`、`quality best` |
| `dir [路徑]` | `cd` | 查看或切換下載儲存路徑，例如：`dir D:\MyMusic` |
| `usb` | - | 自動辨識插上的 USB 隨身碟並切換下載目錄 |
| `check` | - | 檢查目標資料夾是否符合 001 編號格式 |
| `number <on/off>`| `num` | 開啟或關閉檔名 001 前綴序號功能 |
| `open` | - | 在檔案總管開啟當前下載儲存資料夾 |
| `status` | - | 顯示目前系統設定、清單與下載狀態摘要 |
| `clear` | `cls` | 清除命令列控制台輸出畫面 |
| `exit` | `quit` | 關閉應用程式 |

---

## 🛠️ 開發與執行說明

### 1. 本地啟動桌面版（防毒軟體 0 誤判）
點擊外層目錄的 `啟動工具(免防毒誤判).vbs` 或在終端機執行：
```bash
python code/gui_app.py
```

### 2. 重新編譯打包單一 EXE 執行檔
```bash
python -m PyInstaller --onefile --noconsole --name "MediaStream_Downloader" --collect-all customtkinter --add-data "code/ffmpeg_bin;ffmpeg_bin" code/gui_app.py
```
