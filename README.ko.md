<div align="center">

# ⚡ StreamForge
### 고성능 스트리밍 미디어 스튜디오 · 포맷 변환 및 스마트 번호 매기기 도구
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
  <b>8개 국어 실시간 전환 지원 · MP3 / MP4 변환 · USB 자동 감지 · 001 스마트 번호 관리 · 중복 덮어쓰기 방지 · 오류 진단 및 재시도 · 인터랙티브 CLI 내장</b>
</p>

</div>

---

## 🌟 주요 기능 (Key Features)

- 🌐 **완벽한 다국어 인터페이스 지원 (8개 언어)**:
  - **한국어, English, 繁體中文, 简体中文, 日本語, Español, Français, Deutsch** 지원.
  - **설치 마법사 언어 선택**: 설치 파일 실행 시 선호하는 언어를 직접 선택.
  - **앱 내부 실시간 전환**: 오른쪽 상단 메뉴나 정보 창에서 재시작 없이 즉시 언어 변경 가능.
- 🎵 **유연한 멀티 포맷 변환**:
  - **MP3 오디오**: 최대 320 kbps 고음질 변환, ID3 태그 및 앨범 아트 자동 삽입.
  - **🎬 MP4 비디오**: 1080p Full HD 및 720p HD 등 고화질 영상 및 음성 스트림 자동 병합.
- 💾 **USB 드라이브 및 폴더 스마트 번호 매기기 (001, 002...)**:
  - 연결된 USB 드라이브 원클릭 자동 감지.
  - 기존 파일의 번호 형식을 검사하여 다음 번호(예: `016`)부터 자동으로 이어서 번호 부여.
  - 차량용 오디오나 플레이어 재생을 위해 미정리 파일을 `001 - 제목` 형식으로 일괄 정리 지원.
- 🔍 **다운로드 전 중복 검사 및 충돌 방지**:
  - 저장 대상 폴더를 자동 스캔하여 중복 발견 시 **덮어쓰기**, **인덱스 추가 (1)**, **건너뛰기** 옵션 제공.
- ❌ **상세 오류 진단 및 원클릭 재시도**:
  - 비공개 영상, 봇 확인, 403 오류, 타임아웃 등의 오류 원인을 분석하여 표시.
  - 실패한 항목만 클릭 한 번으로 간편하게 재시도.
- 💻 **인터랙티브 CLI 콘솔 탑재**:
  - 키보드 작업자를 위한 터미널 입력 창 제공 (`↑` / `↓` 히스토리 지원).

---

## 🎮 CLI 명령어 목록 (CLI Commands)

하단의 **`💻 실시간 터미널 콘솔`** 에 명령어를 직접 입력하여 제어할 수 있습니다:

| 명령어 | 단축어/별칭 | 기능 설명 및 예시 |
| :--- | :--- | :--- |
| **`about`** | `copyright`, `team` | 버전 및 저작권 정보 표시 |
| **`help`** | `?`, `h` | 사용 가능한 명령어 목록 보기 |
| **`add <URL>`** | `a <URL>` | 단일 곡 또는 재생목록 큐에 추가 (예: `add https://...`) |
| **`paste`** | `p` | 클립보드의 URL을 자동으로 읽어 추가 |
| **`list`** | `ls` | 큐의 모든 항목, 재생 시간, 다운로드 상태 확인 |
| **`select <범위>`** | `sel` | 선택 제어: `select all`, `select none`, `select 1 3 5`, `select 1-5` |
| **`del <범위>`** | `rm` | 항목 제거: `del 2`, `del 1 3`, `del all` |
| **`start`** | `dl`, `run` | 선택된 항목 다운로드 시작 |
| **`pause`** | - | 다운로드 일시정지 |
| **`resume`** | - | 일시정지된 다운로드 재개 |
| **`cancel`** | `stop` | 다운로드 취소 (완료된 파일은 유지) |
| **`retry`** | `r` | 실패한 모든 항목 재시도 |
| **`format <형식>`** | `fmt` | 포맷 전환: `format mp3` 또는 `format mp4` |
| **`quality <값>`** | `q` | 품질 설정: 오디오 `quality 320`, 비디오 `quality 1080` 등 |
| **`dir [경로]`** | `cd` | 다운로드 저장 경로 확인 또는 변경 |
| **`usb`** | - | USB 드라이브를 감지하여 저장 경로로 지정 |
| **`check`** | - | 대상 폴더의 001 번호 매기기 형식 검사 |
| **`number <on/off>`**| `num` | 파일명 앞 001 번호 접두사 활성화/비활성화 |
| **`open`** | - | 탐색기에서 현재 다운로드 폴더 열기 |
| **`status`** | - | 시스템 설정 및 큐 상태 요약 |
| **`clear`** | `cls` | 터미널 화면 지우기 |
| **`exit`** | `quit` | 프로그램 종료 |

---

## 🚀 다운로드 및 설치 (Installation & Releases)

### 1. Windows 설치 프로그램 (권장)
[Releases 페이지](https://github.com/nwchenyw/StreamForge/releases) 에서 최신 **`StreamForge-Setup-v1.1.0.exe`** 를 다운로드하세요:
- **8개 국어 설치 마법사**: 시작 시 한국어를 선택하여 편리하게 설치 진행.
- **자유로운 설치 경로**: 기본 경로 외 외장 하드나 USB 드라이브에도 직접 설치 가능.
- **스크립트 없는 안전한 패키징**: Windows 제어판/설정에서 깔끔하게 원클릭 제거 가능.

### 2. 소스 코드에서 실행 (개발자)
```bash
git clone https://github.com/nwchenyw/StreamForge.git
cd StreamForge
pip install -r code/requirements.txt
python code/gui_app.py
```

---

## ⚖️ 지적 재산권 및 면책 조항 (Legal Disclaimer)

### 저작권 (Copyright Notice)
**© 2026 The StreamForge Team & Contributors. All Rights Reserved.**  
본 프로젝트는 **[MIT License](LICENSE)** 에 따라 오픈소스로 배포됩니다.

### 면책 조항 (Disclaimer)
1. 본 소프트웨어는 개인적인 학습, 연구, 공정 이용 (Fair Use) 및 정당한 개인 백업 용도로 제작된 오픈소스 도구입니다.
2. StreamForge는 저작권 보호 콘텐츠를 호스팅하거나 배포하지 않습니다.
3. 사용자는 관련 저작권 법률 및 각 서비스 이용 약관을 준수할 책임이 있습니다.
