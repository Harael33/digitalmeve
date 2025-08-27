from src.generator import generate_meve, export_public_key, PUBLIC_KEY
import json
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64


def test_generate_meve(tmp_path):
    file_path = tmp_path / "doc.txt"
    file_path.write_text("Hello DigitalMeve")

    meve_file = generate_meve(str(file_path))

    assert os.path.exists(meve_file)

    with open(meve_file, "r", encoding="utf-8") as f:
        data = json.load(f)

        assert data["file"] == "doc.txt"
        assert data["hash"] is not None
        assert data["format"] == "MEVE"
        assert "signature" in data

        # Vérification de la signature
        signature = base64.b64decode(data["signature"].encode())
        PUBLIC_KEY.verify(
            signature,
            json.dumps({k: data[k] for k in ["file","timestamp","hash","algorithm","format"]}, sort_keys=True).encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )


def test_export_public_key(tmp_path):
    path = tmp_path / "pub.pem"
    exported = export_public_key(str(path))
    assert os.path.exists(exported)

    with open(exported, "rb") as f:
        pem = f.read()
        assert b"PUBLIC KEY" in pem
