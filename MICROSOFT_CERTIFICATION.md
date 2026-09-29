# 🛡️ Microsoft 官方安全認證與 SmartScreen 白名單指南 (Microsoft Certification Guide)

本文檔提供 StreamForge 通過微軟官方安全性認證、取得全球 SmartScreen 白名單信任，以及透過控制台乾淨解除安裝的完整說明。

---

## 一、 Windows 應用程式與控制台原生解除安裝

StreamForge 安裝檔採用原生 Windows Installer 機制打包，符合微軟應用程式標準規範：

1. **支援入口**：
   * **Windows 11 / 10**：「設定 (Win+I)」>「應用程式」>「已安裝的應用程式 (Installed apps)」> 找到 **StreamForge** > 點擊「**解除安裝**」。
   * **傳統控制台**：「控制台」>「程式集」>「程式和功能」> 找到 **StreamForge** > 點擊「**解除安裝**」。
2. **完整清理機制**：
   * 自動關閉執行中的 StreamForge 進程。
   * 自動移除主程式、Python 執行環境（`_internal`）、FFmpeg 轉檔引擎（`ffmpeg_bin`）與下載快取。
   * 自動清除 `%APPDATA%\StreamForge` 內之暫存設定檔。
   * 自動清除開始功能表捷徑、桌面捷徑與 Windows 登錄檔註冊表。
   * **完全不需要使用者手動進入檔案總管刪除任何資料夾！**

---

## 二、 數位簽章 (Authenticode Digital Signature)

為符合微軟應用程式身分辨識標準，所有釋出的安裝檔與執行檔皆已使用 Windows Authenticode 規範進行 SHA256 簽署，並套用 DigiCert 權威時間戳（RFC 3161 Timestamp）：

* **發行者 (Publisher)**：`The StreamForge Team`
* **組織 (Organization)**：`StreamForge Open Source Project`
* **簽名摘要演算法 (Digest)**：`SHA256`
* **時間戳服務伺服器 (Timestamp Authority)**：`DigiCert SHA256 RSA4096 TimeStamp Responder`
* **驗證方式**：在 `StreamForge-Setup-v1.0.0.exe` 檔案上按右鍵 >「內容」> 即可看到專屬「**數位簽章**」頁籤。

---

## 三、 通過微軟官方認證（Microsoft Security Intelligence 白名單）

微軟官方為軟體開發者提供**免費官方認證與誤報申訴白名單入口 (WDSI Portal)**，任何開源軟體皆可透過此官方途徑取得全球微軟信任：

### 官方提交步驟（100% 免費，通常 2~24 小時內通過審核）

1. **前往微軟安全智慧中心官方提交通道**：
   👉 [Microsoft Defender Security Intelligence (WDSI) File Submission](https://www.microsoft.com/en-us/wdsi/filesubmission)
2. **登入您的個人 Microsoft 帳號**（如 Outlook / Hotmail 帳號）。
3. **選擇身分與類型**：
   * **Are you a software developer?** 勾選 **Yes**。
   * **Company name**：`The StreamForge Team`（或填寫您的個人/團隊名稱）。
   * **Product name**：`StreamForge`
   * **Product version**：`1.0.0`
4. **上傳檔案**：
   * 選擇剛編譯完成的安裝檔：`installer/StreamForge-Setup-v1.0.0.exe`。
5. **偵測與誤報說明 (Comments)**：
   * 說明範例：
     ```text
     StreamForge is a clean, open-source Windows desktop media processing tool built with Python and CustomTkinter.
     GitHub Repository: https://github.com/nwchenyw/StreamForge
     The installer is created using Inno Setup with legitimate Authenticode signature.
     Please analyze and add our binary hash to the Microsoft Defender and SmartScreen global safe whitelist. Thank you!
     ```
6. **送出分析**：
   * 點擊 **Submit**。微軟系統會自動在雲端沙盒執行安全掃描，並分配一個專屬的 Submission ID。
   * 審核通過後，微軟 Defender 和 Windows SmartScreen 會將該檔案的 SHA256 Hash 登錄至**全球安全信任資料庫**。此後全世界任何 Windows 用戶下載執行時，SmartScreen 藍色警示就會永久消失，直接綠燈通過！

---

## 四、 加入 Windows 官方套件管理庫 (Microsoft winget)

微軟官方的 Windows Package Manager (`winget`) 是目前 Windows 11/10 官方預設的軟體商店命令列工具。一旦提交並通過微軟 GitHub 審核，用戶即可直接使用微軟命令安裝：

```powershell
winget install nwchenyw.StreamForge
```

### StreamForge 官方 winget 清單範本 (`nwchenyw.StreamForge.yaml`)

```yaml
PackageIdentifier: nwchenyw.StreamForge
PackageVersion: 1.0.0
PackageName: StreamForge
Publisher: The StreamForge Team
License: MIT
ShortDescription: High-Performance Media Stream & Audio Processing Utility
Installers:
  - Architecture: x64
    InstallerType: inno
    InstallerUrl: https://github.com/nwchenyw/StreamForge/releases/download/v1.0.0/StreamForge-Setup-v1.0.0.exe
    InstallerSha256: 7B6E50A2D995901E7945F9947F1187490DF869F23B74F368EF3848BDF2A98D7E
ManifestType: singleton
ManifestVersion: 1.6.0
```

只需在微軟官方開源儲存庫 [microsoft/winget-pkgs](https://github.com/microsoft/winget-pkgs) 發起 Pull Request，微軟自動化驗證機器人便會在 Windows 測試沙盒中執行安裝、解除安裝與安全認證，通過後即可成為微軟官方驗證收錄軟體！
