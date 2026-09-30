# StreamForge Playlist Format Specification (`.sfpl`)

**Version:** 1.1  
**MIME-Type:** `application/x-streamforge-playlist`  
**File Extension:** `.sfpl`  
**Standard Encoding:** UTF-8  

---

## 1. 概述 (Overview)
StreamForge 播放清單檔案（`.sfpl`）是專為 StreamForge 設計的現代化、標準化、跨平台播放清單儲存與交換格式。底層採用結構化 JSON，具備強型別驗證、人類可讀性、擴展彈性，並原生相容 YouTube、bilibili、SoundCloud 等串流媒體之詮釋資料。

## 2. 格式結構 (File Structure)

標準 `.sfpl` 檔案包含根物件字典，主要鍵值如下：

```json
{
  "format": "StreamForgePlaylist",
  "version": "1.1",
  "generator": "StreamForge v1.1.0",
  "created_at": "2026-09-30T14:30:00+08:00",
  "playlist_name": "我的最愛音樂精選",
  "total_tracks": 2,
  "settings": {
    "format": "mp3",
    "quality": "320 kbps (最高品質/推薦)",
    "numbering": true
  },
  "tracks": [
    {
      "id": "dQw4w9WgXcQ",
      "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "uploader": "Rick Astley",
      "duration": 213,
      "duration_str": "03:33",
      "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
      "selected": true
    },
    {
      "id": "kJQP7kiw5Fk",
      "title": "Luis Fonsi - Despacito ft. Daddy Yankee",
      "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
      "uploader": "Luis Fonsi",
      "duration": 282,
      "duration_str": "04:42",
      "thumbnail": "https://i.ytimg.com/vi/kJQP7kiw5Fk/hqdefault.jpg",
      "selected": true
    }
  ]
}
```

### 頂層欄位定義 (Header Fields)

| 欄位名稱 | 型別 | 必填 | 說明 |
| :--- | :--- | :---: | :--- |
| `format` | string | 是 | 固定識別字串，必須為 `"StreamForgePlaylist"`。 |
| `version` | string | 是 | 規範版本號，目前為 `"1.1"`。 |
| `generator` | string | 否 | 產出該檔案之軟體名稱與版本號。 |
| `created_at` | string | 否 | ISO 8601 帶時區之建立時間戳記。 |
| `playlist_name` | string | 否 | 歌單名稱。 |
| `total_tracks` | integer | 是 | 歌單內包含的曲目總數。 |
| `settings` | object | 否 | 建議的下載參數（偏好格式、品質、是否開啟編號等）。 |
| `tracks` | array | 是 | 曲目清單陣列。 |

### 曲目物件定義 (Track Object)

| 欄位名稱 | 型別 | 必填 | 說明 |
| :--- | :--- | :---: | :--- |
| `id` | string | 否 | 平台唯一辨識碼（例如 YouTube 11 位元 ID）。 |
| `title` | string | 是 | 曲目標題。 |
| `url` | string | 是 | 串流媒體的完整來源網址。 |
| `uploader` | string | 否 | 上傳者/歌手/頻道名稱。 |
| `duration` | integer | 否 | 歌曲長度（秒數）。 |
| `duration_str` | string | 否 | 格式化時長字串（如 `"03:45"`）。 |
| `thumbnail` | string | 否 | 封面縮圖網址。 |
| `selected` | boolean | 否 | 預設是否勾選下載（預設 `true`）。 |

---

## 3. 相容性與向下支援 (Interoperability)

StreamForge 同時支援匯入以下常見播放清單格式：
1. **`.sfpl`**：原生支援完整詮釋資料、選取狀態與下載設定。
2. **`.json`**：支援一般含 `tracks` 陣列或純 JSON 網址陣列。
3. **`.m3u` / `.m3u8`**：支援讀取 `#EXTINF` 歌手、歌曲長度與音訊網址。
4. **`.txt`**：支援逐行純文字網址（以 `#` 開頭之行視為註解）。

---

## 4. Windows 系統檔案關聯 (File Association)

當 StreamForge 透過 Inno Setup 安裝於 Windows 系統後：
- `.sfpl` 檔案將自動與 `StreamForge.exe` 建立關聯。
- 在檔案總管中雙擊任何 `.sfpl` 檔案，即可直接啟動 StreamForge 並自動載入該播放清單。
