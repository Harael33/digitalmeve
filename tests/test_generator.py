import os
import json
import tempfile
from pathlib import Path

from src.generator import generate_meve

def test_generate_meve_creates_file_and_valid_json():
    with tempfile.TemporaryDirectory() as tmpdir:
        doc = Path(tmpdir) / "sample.txt"
        doc.write_text("hello digitalmeve", encoding="utf-8")

        # génère le .meve
        generate_meve(str(doc))

        meve_path = Path(str(doc) + ".meve")
        assert meve_path.exists(), "Le fichier .meve n'a pas été créé"

        data = json.loads(meve_path.read_text(encoding="utf-8"))

        # champs clés
        assert data["hash_sha256"], "hash_sha256 manquant"
        assert data["time"], "time manquant"
        assert data["status"] in {"Personal", "Pro", "Official"}
        assert data["meta"]["filename"] == "sample.txt"
        assert data["meta"]["size"] == doc.stat().st_size
