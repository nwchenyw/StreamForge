<div align="center">

# ⚡ StreamForge
### Leistungsstarkes Medien-Streaming Studio · Formatkonvertierung & Intelligente Dateinamenverwaltung
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

[![Release](https://img.shields.io/badge/Release-v1.0.0-38bdf8?style=for-the-badge&logo=github)](https://github.com/nwchenyw/StreamForge/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-0284c7?style=for-the-badge&logo=windows)](https://microsoft.com)
[![Python](https://img.shields.io/badge/Python-3.12%2B-f59e0b?style=for-the-badge&logo=python)](https://python.org)
[![i18n](https://img.shields.io/badge/Languages-8%20Supported-purple?style=for-the-badge)](code/i18n.py)

<p align="center">
  <b>Echtzeitunterstützung für 8 Sprachen · MP3 / MP4-Umschaltung · USB-Erkennung · 001-Nummerierung · Duplikat-Vermeidung · Fehlerdiagnose · Interaktives CLI</b>
</p>

</div>

---

## 🌟 Hauptfunktionen (Key Features)

- 🌐 **Umfassende Mehrsprachigkeit (8 Sprachen)**:
  - Vollständige Übersetzung für **Deutsch, English, 繁體中文, 简体中文, 日本語, 한국어, Español und Français**.
  - **Sprachauswahl im Installer**: Bevorzugte Sprache direkt beim Start des Setups wählen.
  - **Dynamische Umschaltung in der App**: Jederzeit oben rechts oder im Infodialog ohne Neustart wechseln.
- 🎵 **Flexible Multi-Format-Konvertierung**:
  - **MP3-Audio**: Bis zu 320 kbps High-Bitrate, automatisches Schreiben von ID3-Tags und Cover-Einbettung.
  - **🎬 MP4-Video**: Bis zu 1080p Full HD und 720p HD mit automatischer Video-/Audio-Zusammenführung.
- 💾 **Intelligente USB-Laufwerks- & Ordnerverwaltung (001, 002...)**:
  - Automatische 1-Klick-Erkennung von eingesteckten USB-Sticks.
  - Fortlaufende Nummerierung basierend auf vorhandenen Dateien (z. B. Weiterführung ab `016`).
  - Vorbereitung unnummerierter Ordner im Format `001 - Titel` für Autoradios und Medienplayer.
- 🔍 **Duplikat-Prüfung vor dem Herunterladen**:
  - Überprüft Zielordner vorab und bietet **Überschreiben**, **Index anhängen (1)** oder **Überspringen** an.
- ❌ **Detaillierte Fehlerdiagnose & 1-Klick-Wiederholung**:
  - Erkennt Ursachen (private Videos, Bot-Prüfungen, 403-Fehler, Timeouts) und wiederholt fehlgeschlagene Elemente mit einem Klick.
- 💻 **Interaktives Terminal (CLI)**:
  - Integrierte Eingabekonsole mit Befehlsverlauf (`↑` / `↓`) für Tastaturbedienung.

---

## 🎮 Befehlsübersicht (CLI Commands)

Steuern Sie StreamForge per Tastatur im Bereich **`💻 Interaktives Terminal`**:

| Befehl | Alias | Beschreibung |
| :--- | :--- | :--- |
| **`about`** | `copyright`, `team` | Version und Lizenzinformationen anzeigen |
| **`help`** | `?`, `h` | Liste aller verfügbaren Befehle anzeigen |
| **`add <URL>`** | `a <URL>` | Einzelnen Titel oder Playlist zur Warteschlange hinzufügen |
| **`paste`** | `p` | URL aus der Zwischenablage einfügen |
| **`list`** | `ls` | Alle Titel in der Warteschlange auflisten |
| **`select <Bereich>`**| `sel` | Titel auswählen: `select all`, `select 1-5` |
| **`del <Bereich>`** | `rm` | Titel aus der Liste entfernen |
| **`start`** | `dl`, `run` | Download ausgewählter Titel starten |
| **`pause`** | - | Laufenden Download anhalten |
| **`resume`** | - | Angehaltenen Download fortsetzen |
| **`cancel`** | `stop` | Download abbrechen (fertige Dateien bleiben erhalten) |
| **`retry`** | `r` | Fehlgeschlagene Elemente erneut versuchen |
| **`format <fmt>`** | `fmt` | Format wechseln: `format mp3` oder `format mp4` |
| **`quality <val>`**| `q` | Qualität festlegen: `quality 320`, `quality 1080` etc. |
| **`dir [Pfad]`** | `cd` | Zielordner anzeigen oder ändern |
| **`usb`** | - | USB-Stick erkennen und Pfad setzen |
| **`open`** | - | Zielordner im Windows-Explorer öffnen |
| **`clear`** | `cls` | Konsolenausgabe leeren |
| **`exit`** | `quit` | Anwendung beenden |

---

## 🚀 Installation & Downloads (Installation & Releases)

### 1. Windows Installer (Empfohlen)
Laden Sie **`StreamForge-Setup-v1.0.0.exe`** von der [Releases-Seite](https://github.com/nwchenyw/StreamForge/releases) herunter:
- Nativer Windows-Installationsassistent in 8 Sprachen.
- Saubere Installation ohne Drittanbieter-Skripte mit vollwertigem Windows-Deinstallationsprogramm.

### 2. Aus Quellcode ausführen
```bash
git clone https://github.com/nwchenyw/StreamForge.git
cd StreamForge
pip install -r code/requirements.txt
python code/gui_app.py
```

---

## ⚖️ Geistiges Eigentum & Haftungsausschluss

**© 2026 The StreamForge Team & Contributors. All Rights Reserved.**  
Lizenziert unter der **[MIT-Lizenz](LICENSE)**.  
StreamForge speichert oder verteilt keine urheberrechtlich geschützten Medien; die Verantwortung liegt beim Nutzer.
