<div align="center">

# ⚡ StreamForge
### Studio Multimédia Haute Performance · Conversion de Formats & Gestion Intelligente des Fichiers
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
  <b>Support de 8 langues en temps réel · Conversion MP3 / MP4 · Détection USB · Numérotation 001 · Prévention des conflits · Console CLI interactive</b>
</p>

</div>

---

## 🌟 Fonctionnalités Principales (Key Features)

- 🌐 **Support Multilingue Intégral (8 langues)** :
  - Interface disponible en **Français, English, 繁體中文, 简体中文, 日本語, 한국어, Español et Deutsch**.
  - **Assistant d'installation multilingue** : Choisissez votre langue dès le lancement de l'installeur.
  - **Changement dynamique dans l'application** : Basculez de langue instantanément depuis le menu supérieur droit sans redémarrer.
- 🎵 **Conversion Multiformat Flexible** :
  - **Audio MP3** : Débit élevé jusqu'à 320 kbps, métadonnées ID3 automatiques et pochette intégrée.
  - **🎬 Vidéo MP4** : Jusqu'à 1080p Full HD et 720p HD avec fusion automatique vidéo et audio.
- 💾 **Gestion Intelligente Clé USB & Dossiers (001, 002...)** :
  - Détection automatique en un clic de la clé USB connectée.
  - Analyse des fichiers existants et continuité automatique de la numérotation (ex. reprise à `016`).
  - Proposition de renommage en `001 - Titre` idéal pour les autoradios et lecteurs portables.
- 🔍 **Résolution des Doublons Avant Téléchargement** :
  - Analyse le dossier de destination et propose d'Écraser, d'Ajouter un suffixe `(1)` ou d'Ignorer les fichiers existants.
- ❌ **Diagnostic Précis et Nouvel Essai en 1 Clic** :
  - Analyse des échecs (vidéos privées, vérification bot, erreur 403, délai dépassé) et relance rapide des éléments en échec.
- 💻 **Console Interactive Intégrée (CLI)** :
  - Invite de commandes avec historique (`↑` / `↓`) pour les utilisateurs avancés.

---

## 🎮 Commandes de la Console (CLI Commands)

Vous pouvez piloter StreamForge au clavier dans le **`💻 Terminal interactif`** :

| Commande | Alias | Description |
| :--- | :--- | :--- |
| **`about`** | `copyright`, `team` | Affiche la version et les mentions légales |
| **`help`** | `?`, `h` | Affiche la liste des commandes disponibles |
| **`add <URL>`** | `a <URL>` | Ajoute une piste ou une playlist à la file |
| **`paste`** | `p` | Ajoute l'URL présente dans le presse-papier |
| **`list`** | `ls` | Liste les éléments de la file d'attente |
| **`select <plage>`**| `sel` | Sélectionne des pistes : `select all`, `select 1-5` |
| **`del <plage>`** | `rm` | Supprime des éléments de la file |
| **`start`** | `dl`, `run` | Lance le téléchargement des pistes sélectionnées |
| **`pause`** | - | Met en pause les téléchargements |
| **`resume`** | - | Reprend les téléchargements |
| **`cancel`** | `stop` | Annule les téléchargements en cours |
| **`retry`** | `r` | Réessaie tous les éléments en échec |
| **`format <fmt>`** | `fmt` | Change de format : `format mp3` ou `format mp4` |
| **`quality <val>`**| `q` | Règle la qualité : `quality 320`, `quality 1080` |
| **`dir [chemin]`** | `cd` | Affiche ou modifie le dossier de destination |
| **`usb`** | - | Détecte la clé USB et bascule le dossier |
| **`open`** | - | Ouvre le dossier dans l'Explorateur Windows |
| **`clear`** | `cls` | Efface la console |
| **`exit`** | `quit` | Quitte l'application |

---

## 🚀 Installation & Téléchargement (Installation & Releases)

### 1. Programme d'installation Windows (Recommandé)
Téléchargez **`StreamForge-Setup-v1.1.0.exe`** depuis la page [Releases](https://github.com/nwchenyw/StreamForge/releases) :
- Assistant natif disponible en 8 langues.
- Installation propre sans script masqué, désinstallable en un clic via les Paramètres Windows.

### 2. Exécution depuis les sources
```bash
git clone https://github.com/nwchenyw/StreamForge.git
cd StreamForge
pip install -r code/requirements.txt
python code/gui_app.py
```

---

## ⚖️ Propriété Intellectuelle & Mentions Légales

**© 2026 The StreamForge Team & Contributors. All Rights Reserved.**  
Distribué sous licence open source **[MIT](LICENSE)**.  
StreamForge n'héberge aucun contenu protégé ; l'utilisateur est seul responsable de son utilisation.
