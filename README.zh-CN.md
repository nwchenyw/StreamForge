<div align="center">

# ⚡ StreamForge
### 高性能流媒体影音工坊 · 跨格式转换与智能文件名管理工具
**High-Performance Media Stream & Audio Processing Utility**

<p align="center">
  <a href="README.md"><b>繁體中文</b></a> •
  <a href="README.en.md"><b>English</b></a> •
  <a href="README.zh-CN.md"><b>简体中文</b></a> •
  <a href="README.ja.md"><b>日本語</b></a> •
  <a href="README.ko.md"><b>한국어</b></a> •
  <a href="README.es.md"><b>Español</b></a> •
  <a href="README.fr.md"><b>Français</b></a> •
  <a href="README.de.md"><b>Deutsch</b></a>
</p>

[![Release](https://img.shields.io/badge/Release-v1.1.0-38bdf8?style=for-the-badge&logo=github)](https://github.com/nwchenyw/StreamForge/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-0284c7?style=for-the-badge&logo=windows)](https://microsoft.com)
[![Python](https://img.shields.io/badge/Python-3.12%2B-f59e0b?style=for-the-badge&logo=python)](https://python.org)
[![i18n](https://img.shields.io/badge/Languages-8%20Supported-purple?style=for-the-badge)](code/i18n.py)

<p align="center">
  <b>支持 8 国语言即时切换 · MP3 / MP4 切换 · U盘智能识别 · 001 顺序编号 · 目标目录防覆盖查重 · 失败诊断与一键重试 · 内置交互式命令行 (CLI)</b>
</p>

</div>

---

## 🌟 核心特色 (Key Features)

- 🌐 **多国语言界面 (8 国语言支持)**：
  - 支持 **简体中文、繁體中文、English、日本語、한국어、Español、Français、Deutsch**。
  - **安装向导支持多语言**：启动安装包时即可自选首选语言。
  - **应用内随时动态切换**：在主窗口右上角或“关于 / 授权”对话框中一键切换，文字即时更新，无需重启。
- 🎵 **多格式灵活切换**：
  - **MP3 纯音频**：最高 320 kbps 高音质转码，自动写入 ID3 歌曲标签与内嵌专辑封面。
  - **🎬 MP4 视频**：支持最高画质（1080p Full HD / 720p HD 等），自动合并高清视频与音频流。
- 💾 **U盘与文件夹智能编号检查 (001, 002...)**：
  - 一键自动检测插入的 U盘。
  - 智能检查现有文件编号格式，新文件自动接续编号（例如从 `016` 顺延）。
  - 若文件未编号，主动询问是否自动二阶段重命名为 `001 - 文件名`（适合车载音响或播放器）。
- 🔍 **下载前智能查重防覆盖**：
  - 下载前自动扫描目标文件夹，发现同名或相同歌曲时弹窗提供 **覆盖**、**追加编号后缀 (1)** 或 **跳过**，支持“应用到全部”。
- ❌ **失败详细诊断与一键重试**：
  - 自动捕获并分析每首歌曲失败原因（如私人视频、平台验证、HTTP 403 限速或网络超时）。
  - 一键重试所有失败项目，无需手动重新添加。
- 💻 **交互式命令行控制台 (Interactive CLI Prompt)**：
  - 专为极客与进阶用户打造的操作面板，支持快捷指令、执行日志流与 `↑` / `↓` 历史命令切换。
- 🛡️ **反爬虫强化与稳定连接**：
  - 内置多平台移动端 API 模拟机制，大幅降低服务器验证失败率，内置 10 次自动重试。

---

## 🎮 控制台指令一览表 (CLI Commands)

您可以在工具下方的 **`💻 实时命令行状态`** 输入指令，完全使用键盘进行控制：

| 指令 | 简称/别名 | 功能说明与示例 |
| :--- | :--- | :--- |
| **`about`** | `copyright`, `team` | 显示 StreamForge 软件版本与知识产权声明 |
| **`help`** | `?`, `h` | 显示所有可用指令与说明 |
| **`add <网址>`** | `a <网址>` | 添加单曲或播放列表网址至列表中（例如：`add https://...`） |
| **`paste`** | `p` | 自动读取系统剪贴板中的网址并加入 |
| **`list`** | `ls` | 列出当前列表中所有歌曲、时长、勾选与下载状态 |
| **`select <范围>`** | `sel` | 选择歌曲：`select all`、`select none`、`select 1 3 5`、`select 1-5` |
| **`del <范围>`** | `rm` | 删除歌曲：`del 2`、`del 1 3`、`del all` |
| **`start`** | `dl`, `run` | 启动批量下载所有已勾选的歌曲 |
| **`pause`** | - | 暂停当前下载任务 |
| **`resume`** | - | 恢复已暂停的下载任务 |
| **`cancel`** | `stop` | 取消当前下载任务（保留已完成文件） |
| **`retry`** | `r` | 重新尝试下载所有标记为失败的歌曲 |
| **`format <格式>`** | `fmt` | 切换格式：`format mp3` 或 `format mp4` |
| **`quality <值>`** | `q` | 设置质量：音质 `quality 320` 或画质 `quality 1080`、`quality best` |
| **`dir [路径]`** | `cd` | 查看或切换下载保存路径，例如：`dir D:\MyMusic` |
| **`usb`** | - | 自动识别插入的 U盘并切换下载目录 |
| **`check`** | - | 检查目标文件夹是否符合 001 编号格式 |
| **`number <on/off>`**| `num` | 开启或关闭文件名 001 前缀序号功能 |
| **`open`** | - | 在资源管理器中打开当前下载保存文件夹 |
| **`status`** | - | 显示当前系统设置、列表与下载状态摘要 |
| **`clear`** | `cls` | 清除命令行控制台输出画面 |
| **`exit`** | `quit` | 退出应用程序 |

---

## 🚀 下载与安装 (Installation & Releases)

### 1. Windows 原生多语言安装包 (推荐)
前往 [Releases 页面](https://github.com/nwchenyw/StreamForge/releases) 下载最新版的 **`StreamForge-Setup-v1.1.0.exe`**：
- **8 国语言安装向导**：启动安装程序时即可自选界面语言。
- **自定义安装路径**：可自由安装于默认系统路径、任意硬盘目录或 U盘。
- **快捷方式设置**：安装时可自选是否创建桌面与开始菜单快捷方式。
- **自动更新检查**：安装向导与应用设置中均可开启“启动时自动检查最新版本”。
- **纯净无脚本**：标准 Windows 原生安装向导，附带干净的卸载程序（可在“设置 > 应用”一键移除）。

### 2. 从源码运行 (开发者模式)
```bash
# 克隆仓库
git clone https://github.com/nwchenyw/StreamForge.git
cd StreamForge

# 安装依赖
pip install -r code/requirements.txt

# 启动应用程序
python code/gui_app.py
```

### 3. 本地编译 Windows 安装包
```bash
# 步骤 1: 打包应用程序目录
python -m PyInstaller --onedir --noconsole --name "StreamForge" --collect-all customtkinter --add-data "code/ffmpeg_bin;ffmpeg_bin" code/gui_app.py --clean -y

# 步骤 2: 编译 Inno Setup 多语言安装文件
iscc .github/installer/installer.iss
# 生成的安装文件位于 installer/StreamForge-Setup-v1.1.0.exe
```

---

## ⚖️ 知识产权与法律免责声明 (Legal Disclaimer)

### 版权宣告 (Copyright Notice)
**© 2026 The StreamForge Team & Contributors. All Rights Reserved.**  
本项目基于 **[MIT License](LICENSE)** 授权开源。

### 免责声明 (Disclaimer)
1. 本项目为开源软件，开发目的仅供**个人学习、研究、合理使用 (Fair Use) 以及备份个人合法内容**。
2. 本项目**不提供、不存储、亦不分发**任何受版权保护的媒体内容，所有下载数据均由用户提供的网络链接实时流式处理。
3. 用户使用本工具时，应当自觉遵守所在国家/地区的法律法规以及各音视频平台的服务协议。
4. 任何因不当使用、商业营利或侵犯他人知识产权所产生的法律责任，概由用户自行承担，开发团队不承担任何连带担保或法律责任。
