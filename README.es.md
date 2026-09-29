<div align="center">

# ⚡ StreamForge
### Taller Multimedia de Alto Rendimiento · Conversión de Formatos y Gestión Inteligente de Nombres
**High-Performance Media Stream & Audio Processing Utility**

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
  <b>Soporte para 8 idiomas en tiempo real · Conversión MP3 / MP4 · Detección de USB · Numeración 001 · Prevención de conflictos · Consola CLI interactiva</b>
</p>

</div>

---

## 🌟 Características Principales (Key Features)

- 🌐 **Soporte Multilingüe Completo (8 idiomas)**:
  - Disponible en **Español, English, 繁體中文, 简体中文, 日本語, 한국어, Français y Deutsch**.
  - **Selector de idioma en el instalador**: Elija su idioma favorito directamente en el asistente de instalación.
  - **Cambio dinámico en la aplicación**: Cambie de idioma al instante desde la esquina superior derecha o desde el diálogo "Acerca de" sin reiniciar.
- 🎵 **Conversión flexible multiformato**:
  - **Audio MP3**: Hasta 320 kbps de alta fidelidad, metadatos ID3 automáticos y portada incrustada.
  - **🎬 Video MP4**: Hasta 1080p Full HD y 720p HD con fusión automática de video y audio.
- 💾 **Gestión inteligente de USB y numeración (001, 002...)**:
  - Detección automática en un clic de memorias USB conectadas.
  - Inspecciona la numeración existente y continúa la secuencia automáticamente (por ejemplo, desde `016`).
  - Permite renombrar carpetas no numeradas al formato `001 - Título` para sistemas de sonido y reproductores de automóviles.
- 🔍 **Resolución de duplicados antes de la descarga**:
  - Escanea la carpeta de destino y ofrece opciones de **Sobrescribir**, **Añadir sufijo (1)** o **Omitir** (con opción "Aplicar a todo").
- ❌ **Diagnóstico detallado y reintento en un clic**:
  - Clasifica las causas de fallos (videos privados, bloqueos bot, error 403, tiempo de espera agotado) y permite reintentar solo los fallidos.
- 💻 **Consola de comandos interactiva (CLI)**:
  - Panel de terminal integrado para usuarios avanzados con historial de comandos (`↑` / `↓`).

---

## 🎮 Comandos de la Consola (CLI Commands)

Puede interactuar completamente por teclado ingresando comandos en el **`💻 Terminal interactivo`**:

| Comando | Alias | Descripción |
| :--- | :--- | :--- |
| **`about`** | `copyright`, `team` | Muestra versión, derechos de autor y licencia |
| **`help`** | `?`, `h` | Muestra lista de comandos disponibles |
| **`add <URL>`** | `a <URL>` | Añade pista o lista de reproducción a la cola |
| **`paste`** | `p` | Lee la URL del portapapeles y la añade |
| **`list`** | `ls` | Lista los elementos en cola y su estado |
| **`select <rango>`**| `sel` | Selección: `select all`, `select none`, `select 1-5` |
| **`del <rango>`** | `rm` | Eliminar elementos de la cola |
| **`start`** | `dl`, `run` | Inicia la descarga de los elementos seleccionados |
| **`pause`** | - | Pausa la descarga activa |
| **`resume`** | - | Reanuda la descarga pausada |
| **`cancel`** | `stop` | Cancela la descarga en curso |
| **`retry`** | `r` | Reintenta todos los elementos fallidos |
| **`format <fmt>`** | `fmt` | Cambia formato: `format mp3` o `format mp4` |
| **`quality <val>`**| `q` | Ajusta calidad: `quality 320`, `quality 1080`, etc. |
| **`dir [ruta]`** | `cd` | Consulta o cambia la carpeta de destino |
| **`usb`** | - | Detecta unidad USB y cambia la ruta |
| **`check`** | - | Comprueba el formato de numeración 001 |
| **`open`** | - | Abre la carpeta de destino en el Explorador de Windows |
| **`clear`** | `cls` | Limpia la consola |
| **`exit`** | `quit` | Cierra la aplicación |

---

## 🚀 Instalación y Descargas (Installation & Releases)

### 1. Instalador nativo para Windows (Recomendado)
Descargue **`StreamForge-Setup-v1.0.0.exe`** desde la sección [Releases](https://github.com/nwchenyw/StreamForge/releases):
- Asistente de instalación nativo en 8 idiomas.
- Instalación limpia sin scripts innecesarios, con desinstalador estándar.

### 2. Ejecutar desde código fuente
```bash
git clone https://github.com/nwchenyw/StreamForge.git
cd StreamForge
pip install -r code/requirements.txt
python code/gui_app.py
```

---

## ⚖️ Aviso Legal y Propiedad Intelectual

**© 2026 The StreamForge Team & Contributors. All Rights Reserved.**  
Distribuido bajo licencia **[MIT](LICENSE)**.
StreamForge no aloja ni distribuye contenido protegido; los usuarios son responsables del cumplimiento legal.
