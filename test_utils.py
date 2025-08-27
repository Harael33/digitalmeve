# tests/test_utils.py
import os, tempfile
from src.utils import sha256_file, b64, utc_now_iso, file_meta

def test_sha256_file_roundtrip():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"hello-meve")
        path = tmp.name
    try:
        h = sha256_file(path)
        # hash pré-calculé
        assert h == "2d0c3ccebf8833b0e0f33c87b3755890a5a2e0d5bb0c25d4f410c2a0c47a5a9d"
    finally:
        os.remove(path)

def test_b64():
    assert b64(b"MEVE") == "TUVWRQ=="

def test_utc_now_iso_format():
    s = utc_now_iso()
    assert s.endswith("Z") and "T" in s and len(s) >= 20

def test_file_meta():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"x"*10)
        path = tmp.name
    try:
        meta = file_meta(path)
        assert meta["size"] == 10
        assert "name" in meta and "mime" in meta
    finally:
        os.remove(path)
