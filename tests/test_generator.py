import os
import tempfile

from src.generator import generate_meve
from src.utils import sha256_file, load_json

def test_generate_meve_creates_file_and_valid_content():
    # crée un fichier temporaire
    with tempfile.TemporaryDirectory() as tmp:
        doc = os.path.join(tmp, "sample.txt")
        with open(doc, "w", encoding="utf-8") as f:
            f.write("hello MEVE")

        out_path, meve = generate_meve(doc, issuer="tester@example.com", status="Personal")

        assert os.path.exists(out_path)
        # charge le .meve écrit
        on_disk = load_json(out_path)

        # hash attendu = hash du doc
        expected_hash = sha256_file(doc)
        assert on_disk["hash_sha256"] == expected_hash
        assert on_disk["spec"] == "MEVE/1"
        assert on_disk["status"] == "Personal"
        assert on_disk["issuer"] == "tester@example.com"
        assert on_disk["meta"]["original_name"] == "sample.txt"
