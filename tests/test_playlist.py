# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import pytest

# 加入 code 目錄至 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "code")))
import playlist


@pytest.fixture
def sample_songs():
    return [
        {
            "id": "dQw4w9WgXcQ",
            "title": "Rick Astley - Never Gonna Give You Up",
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "uploader": "Rick Astley",
            "duration": 213,
            "duration_str": "03:33",
            "thumbnail": "https://example.com/thumb1.jpg",
            "selected": True,
        },
        {
            "id": "kJQP7kiw5Fk",
            "title": "Luis Fonsi - Despacito ft. Daddy Yankee",
            "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
            "uploader": "Luis Fonsi",
            "duration": 282,
            "duration_str": "04:42",
            "thumbnail": "https://example.com/thumb2.jpg",
            "selected": False,
        }
    ]


def test_save_and_load_sfpl(sample_songs):
    with tempfile.NamedTemporaryFile(suffix=".sfpl", delete=False, encoding="utf-8", mode="w") as f:
        tmp_path = f.name

    try:
        ok, msg = playlist.save_playlist(tmp_path, sample_songs, playlist_name="測試清單")
        assert ok is True
        assert os.path.exists(tmp_path)

        success, loaded_tracks, info = playlist.load_playlist(tmp_path)
        assert success is True
        assert len(loaded_tracks) == 2
        assert loaded_tracks[0]["id"] == "dQw4w9WgXcQ"
        assert loaded_tracks[0]["title"] == "Rick Astley - Never Gonna Give You Up"
        assert loaded_tracks[0]["uploader"] == "Rick Astley"
        assert loaded_tracks[1]["id"] == "kJQP7kiw5Fk"
        assert loaded_tracks[1]["duration_str"] == "04:42"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_save_and_load_m3u8(sample_songs):
    with tempfile.NamedTemporaryFile(suffix=".m3u8", delete=False, encoding="utf-8", mode="w") as f:
        tmp_path = f.name

    try:
        ok, msg = playlist.save_playlist(tmp_path, sample_songs, playlist_name="M3U8測試")
        assert ok is True

        success, loaded_tracks, info = playlist.load_playlist(tmp_path)
        assert success is True
        assert len(loaded_tracks) == 2
        assert loaded_tracks[0]["url"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        assert "Rick Astley" in loaded_tracks[0]["uploader"]
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_save_and_load_txt(sample_songs):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, encoding="utf-8", mode="w") as f:
        tmp_path = f.name

    try:
        ok, msg = playlist.save_playlist(tmp_path, sample_songs)
        assert ok is True

        success, loaded_tracks, info = playlist.load_playlist(tmp_path)
        assert success is True
        assert len(loaded_tracks) == 2
        assert loaded_tracks[0]["url"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_empty_or_invalid_file():
    with tempfile.NamedTemporaryFile(suffix=".sfpl", delete=False, encoding="utf-8", mode="w") as f:
        f.write("")
        tmp_path = f.name

    try:
        success, tracks, msg = playlist.load_playlist(tmp_path)
        assert success is False
        assert len(tracks) == 0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
