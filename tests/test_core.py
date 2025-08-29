# tests/test_core.py
import json
import os
from pathlib import Path

from digitalmeve.core import generate_meve, verify_meve


ISSUER = "DigitalMeve Test Suite"


def _assert_meve_dict(meve: dict, original: bytes, filename: str):
    # Clés de haut niveau
    for key in ("meve_version", "created_at", "issuer", "subject"):
        assert key in meve, f"Missing key '{key}' in MEVE: {meve}"

    assert isinstance(meve["subject"], dict), "subject must be a dict"
    subj = meve["subject"]

    # Clés sujet
    for key in ("mime", "sha256", "filename"):
        assert key in subj, f"Missing subject.{key} in MEVE"

    # Nom de fichier
    assert Path(subj["filename"]).name == Path(filename).name

    # Hash doit être une hex string de 64 chars
    h = subj["sha256"]
    assert isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdef" for c in h), \
        f"Invalid sha256: {h}"


def test_generate_meve_in_memory(tmp_path):
    """Génère une preuve en mémoire (sans outfile) et vérifie la structure."""
    infile = tmp_path / "sample.txt"
    infile.write_text("hello meve\n", encoding="utf-8")

    # API d’après les logs: generate_meve(infile, outfile, issuer) -> dict
    meve = generate_meve(str(infile), None, ISSUER)

    assert isinstance(meve, dict), f"generate_meve should return dict, got {type(meve)}"
    _assert_meve_dict(meve, infile.read_bytes(), infile.name)
    assert meve["issuer"] == ISSUER


def test_generate_and_verify_valid(tmp_path):
    """Génère une preuve sur disque puis vérifie avec verify_meve()."""
    infile = tmp_path / "sample.txt"
    infile.write_text("hello meve\n", encoding="utf-8")

    outfile = tmp_path / (infile.name + ".meve.json")
    meve = generate_meve(str(infile), str(outfile), ISSUER)

    # Fichier écrit
    assert outfile.exists(), "outfile should be created by generate_meve"

    # verify_meve(file, expected_issuer) -> (ok, info)
    ok, info = verify_meve(str(outfile), expected_issuer=ISSUER)
    assert ok is True, f"Expected verification ok=True, got {ok}, info={info}"
    assert isinstance(info, dict), "info should be MEVE dict on success"
    _assert_meve_dict(info, infile.read_bytes(), infile.name)
    assert info["issuer"] == ISSUER


def test_verify_meve_rejects_invalid_issuer(tmp_path):
    """Altère l’issuer pour s’assurer que verify_meve refuse la preuve."""
    infile = tmp_path / "sample.txt"
    infile.write_text("hello meve\n", encoding="utf-8")

    outfile = tmp_path / (infile.name + ".meve.json")
    meve = generate_meve(str(infile), str(outfile), ISSUER)
    assert outfile.exists()

    # Corruption contrôlée : change l’issuer
    data = json.loads(outfile.read_text(encoding="utf-8"))
    data["issuer"] = "Attacker Inc."
    corrupt = tmp_path / (infile.name + ".corrupt.meve.json")
    corrupt.write_text(json.dumps(data), encoding="utf-8")

    ok, info = verify_meve(str(corrupt), expected_issuer=ISSUER)
    assert ok is False, "Corrupted proof should fail verification"

    # Selon l’implémentation actuelle, info peut être str (message) ou dict({error:...})
    assert isinstance(info, (str, dict)), f"Unexpected info type on failure: {type(info)}"
    if isinstance(info, dict):
        # Optionnel : vérifier qu’on a une clé d’erreur
        assert "error" in info or "reason" in info or "message" in info
