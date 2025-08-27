import os
import json
import hashlib
import tempfile

from src.generator import generate_meve
from src.verifier import verify_meve, read_meve_info


def _sha256_hex(path: str) -> str:
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def test_verify_meve_ok_and_ko():
    """
    Scénario:
      1) Génère un .MEVE pour un document -> vérification doit être True
      2) Modifie le document -> vérification doit être False
    On loggue en cas d'échec: issuer, hash attendu, hash recalculé, chemins.
    """
    with tempfile.TemporaryDirectory() as tmp:
        doc = os.path.join(tmp, "doc.txt")
        with open(doc, "wb") as f:
            f.write(b"hello meve")

        # Génération avec issuer explicite (nouveau paramètre)
        issuer = "tester@example.com"
        meve_path = generate_meve(doc, issuer=issuer)

        # Lecture d'info MEVE pour debug/assurances
        info = read_meve_info(meve_path)
        assert info.get("Issuer") == issuer, (
            f"Issuer incorrect dans MEVE. Attendu={issuer} / Lu={info.get('Issuer')}"
        )
        assert "Hash-SHA256" in info, "Le champ 'Hash-SHA256' doit être présent dans le MEVE."

        # 1) Cas OK
        ok = verify_meve(doc, meve_path)
        if not ok:
            recalculated = _sha256_hex(doc)
            expected = info.get("Hash-SHA256")
            raise AssertionError(
                "verify_meve devrait retourner True mais a retourné False.\n"
                f"Issuer: {info.get('Issuer')}\n"
                f"Chemin document: {doc}\n"
                f"Chemin MEVE: {meve_path}\n"
                f"Hash attendu (MEVE): {expected}\n"
                f"Hash recalculé (doc): {recalculated}\n"
            )

        # 2) Cas KO (on modifie le document)
        with open(doc, "ab") as f:
            f.write(b" -- modif")

        ko = verify_meve(doc, meve_path)
        if ko:
            recalculated = _sha256_hex(doc)
            expected = info.get("Hash-SHA256")
            raise AssertionError(
                "verify_meve devrait retourner False après modification du document.\n"
                f"Issuer: {info.get('Issuer')}\n"
                f"Chemin document: {doc}\n"
                f"Chemin MEVE: {meve_path}\n"
                f"Hash attendu (MEVE): {expected}\n"
                f"Hash recalculé (doc modifié): {recalculated}\n"
            )


def test_read_meve_info_minimal_fields():
    """
    Vérifie que read_meve_info retourne au moins les champs clés et qu'ils sont cohérents.
    """
    with tempfile.TemporaryDirectory() as tmp:
        doc = os.path.join(tmp, "a.pdf")
        with open(doc, "wb") as f:
            f.write(b"%PDF-1.4\nMEVE")

        meve = generate_meve(doc, issuer="tester@example.com")
        data = read_meve_info(meve)

        for key in ("Status", "Issuer", "Certified", "Time", "Hash-SHA256", "ID", "Meta"):
            assert key in data, f"Le champ '{key}' doit exister dans le MEVE."

        # Hash cohérent
        assert data["Hash-SHA256"] == _sha256_hex(doc), "Hash du MEVE incohérent avec le document."

        # Meta cohérentes (nom et taille)
        meta = data.get("Meta", "")
        assert os.path.basename(doc) in meta, f"Le nom du fichier devrait apparaître dans Meta. Meta={meta}"
        assert str(os.path.getsize(doc)) in meta, f"La taille du fichier devrait apparaître dans Meta. Meta={meta}"
