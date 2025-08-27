import os
import tempfile

from src.generator import generate_meve
from src.verifier import verify_meve

def test_verify_meve_ok_and_ko():
    with tempfile.TemporaryDirectory() as tmp:
        # doc original
        doc = os.path.join(tmp, "original.txt")
        with open(doc, "w", encoding="utf-8") as f:
            f.write("hello MEVE")

        meve_path, _ = generate_meve(doc, issuer="tester@example.com")

        # Vérification OK
        ok, info = verify_meve(doc, meve_path)
        assert ok is True
        assert info["ok"] is True
        assert info["status"] == "Personal"

        # Modifie le document => Vérification KO
        with open(doc, "a", encoding="utf-8") as f:
            f.write(" (tampered)")
        ok2, info2 = verify_meve(doc, meve_path)
        assert ok2 is False
        assert info2["ok"] is False
        assert info2["expected"] != info2["actual"]
