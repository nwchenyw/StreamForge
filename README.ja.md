<div align="center">

# ⚡ StreamForge
### 高性能ストリーミングメディア工房 · 形式変換＆スマート連番管理ツール
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
  <b>8ヶ国語リアルタイム切替対応 · MP3 / MP4 変換 · USB 自動検出 · 001 連番管理 · 重複防止 · エラー診断＆再試行 · 対話型 CLI 搭載</b>
</p>

</div>

---

## 🌟 主な機能 (Key Features)

- 🌐 **充実の多言語サポート (8ヶ国語)**:
  - **日本語、English、繁體中文、简体中文、한국어、Español、Français、Deutsch** に完全対応。
  - **インストーラーの言語選択**: セットアップ起動時に希望の言語を選択可能。
  - **アプリ内リアルタイム切替**: 右上メニューまたは情報ダイアログから再起動なしで即座に言語変更。
- 🎵 **柔軟なマルチフォーマット変換**:
  - **MP3 音声**: 最大 320 kbps の高音質変換、ID3 タグおよびアルバムアートワークの自動埋め込み。
  - **🎬 MP4 動画**: 最高画質（1080p Full HD、720p HD など）に対応、映像と音声を自動統合。
- 💾 **USB メモリとフォルダ連番スマート管理 (001, 002...)**:
  - 接続された USB メモリをワンクリックで自動認識。
  - 既存ファイルの番号を解析し、連続した連番（例: `016` から再開）を自動付加。
  - 連番が付いていないフォルダに対し、カーオーディオやプレイヤー向けに `001 - タイトル` 形式への一括変更を提案。
- 🔍 **ダウンロード前の重複チェックと競合解決**:
  - 保存先を自動走査し、同名ファイルが存在する場合は「上書き」「別名保存 (1)」「スキップ」を個別または一括で選択。
- ❌ **詳細なエラー診断とワンクリック再試行**:
  - 失敗原因（非公開動画、認証、403 エラー、タイムアウト）を自動解析して表示。
  - 失敗した項目だけをワンクリックで再試行可能。
- 💻 **対話型コマンドラインコンソール (Interactive CLI)**:
  - キーボード派向けの高速ターミナルパネルを搭載。コマンド履歴（`↑` / `↓`）に対応。

---

## 🎮 コマンド一覧 (CLI Commands)

画面下部の **`💻 インタラクティブターミナル`** に直接入力して操作できます：

| コマンド | 短縮/別名 | 説明・使用例 |
| :--- | :--- | :--- |
| **`about`** | `copyright`, `team` | バージョン、ライセンス、著作権情報の表示 |
| **`help`** | `?`, `h` | 利用可能なコマンド一覧の表示 |
| **`add <URL>`** | `a <URL>` | 単曲またはプレイリストの追加（例: `add https://...`） |
| **`paste`** | `p` | クリップボードから URL を読み取って追加 |
| **`list`** | `ls` | キュー内の全メディア、再生時間、ステータスを一覧表示 |
| **`select <範囲>`** | `sel` | 選択操作: `select all`、`select none`、`select 1 3 5`、`select 1-5` |
| **`del <範囲>`** | `rm` | 削除操作: `del 2`、`del 1 3`、`del all` |
| **`start`** | `dl`, `run` | 選択項目のダウンロードを一括開始 |
| **`pause`** | - | ダウンロードを一時停止 |
| **`resume`** | - | 一時停止したダウンロードを再開 |
| **`cancel`** | `stop` | ダウンロードを中止（完了済みファイルは保持） |
| **`retry`** | `r` | 失敗した項目をすべて再試行 |
| **`format <形式>`** | `fmt` | 形式変更: `format mp3` または `format mp4` |
| **`quality <値>`** | `q` | 品質変更: `quality 320` または動画 `quality 1080`、`quality best` |
| **`dir [パス]`** | `cd` | 保存先フォルダの確認または変更（例: `dir D:\Music`） |
| **`usb`** | - | USB ドライブを自動検出して保存先に設定 |
| **`check`** | - | 保存先フォルダの 001 連番フォーマットを検査 |
| **`number <on/off>`**| `num` | ファイル名先頭の 001 連番付加を有効/無効化 |
| **`open`** | - | 保存先フォルダをエクスプローラーで開く |
| **`status`** | - | 現在の設定とキュー状態の要約を表示 |
| **`clear`** | `cls` | ターミナル画面をクリア |
| **`exit`** | `quit` | アプリケーションを終了 |

---

## 🚀 ダウンロードとインストール (Installation & Releases)

### 1. Windows インストーラー (推奨)
[Releases ページ](https://github.com/nwchenyw/StreamForge/releases) から最新の **`StreamForge-Setup-v1.1.0.exe`** をダウンロードしてください：
- **8ヶ国語ウィザード**: インストール開始時に日本語を含む 8 言語から選択可能。
- **インストール先の自由選択**: 標準パス、外部ドライブ、USB メモリなど自由な場所に導入可能。
- **自動アップデート確認**: 起動時の最新版確認をいつでも設定可能。
- **安心・クリーン設計**: Windows 標準のアンインストーラーが付属（設定の「アプリ」から簡単に削除可能）。

### 2. ソースコードから実行 (開発者向け)
```bash
git clone https://github.com/nwchenyw/StreamForge.git
cd StreamForge
pip install -r code/requirements.txt
python code/gui_app.py
```

---

## ⚖️ 知的財産権と法的免責事項 (Legal Disclaimer)

### 著作権表示 (Copyright Notice)
**© 2026 The StreamForge Team & Contributors. All Rights Reserved.**  
本プロジェクトは **[MIT License](LICENSE)** に基づいて公開されています。

### 免責事項 (Disclaimer)
1. 本ソフトウェアは、個人の学習、研究、フェアユース（公正利用）、および合法的な個人バックアップ目的でのみ利用されることを意図したオープンソースツールです。
2. StreamForge は著作権で保護されたコンテンツを保持・配信・ホストしません。
3. 利用者は、各配信プラットフォームの利用規約および適用される著作権法を遵守してください。
