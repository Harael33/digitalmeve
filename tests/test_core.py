# tests/test_core.py
import json
from pathlib import Path
from digitalmeve.core import generate_meve, verify_meve

ISSUER = "DigitalMeve Test Suite"


def _assert_meve_dict(meve: dict, filename: str):
    """Vérifie la structure MEVE renvoyée (qui contient un champ raw)."""
    assert "raw" in meve, f"MEVE dict should contain 'raw', got {meve.keys()}"
    raw = meve["raw"]

    # Clés obligatoires
    for key in ("meve_version", "created_at", "issuer", "subject"):
        assert key in raw, f"Missing key '{key}' in MEVE.raw: {raw}"

    subj = raw["subject"]
    for key in ("mime", "sha256", "filename"):
        assert key in subj, f"Missing subject.{key} in MEVE.raw"

    # Nom du fichier
    assert Path(subj["filename"]).name == Path(filename).name
    # Hash doit ressembler à un SHA256
    h = subj["sha256"]
    assert isinstance(h, str) and len(h) == 64 and all(c in "0123456789abcdef" for c in h)


def test_generate_and_verify_valid(tmp_path):
    """Génère une preuve puis la valide avec verify_meve()."""
    infile = tmp_path / "sample.txt"
    infile.write_text("hello meve\n", encoding="utf-8")

    outfile = tmp_path / (infile.name + ".meve.json")
    meve = generate_meve(str(infile), str(outfile), ISSUER)
    assert outfile.exists(), "outfile should be created"

    # Vérifie la structure du dict renvoyé
    assert isinstance(meve, dict)
    _assert_meve_dict(meve, infile.name)

    # Vérifie avec verify_meve
    ok, info = verify_meve(str(outfile), expected_issuer=ISSUER)
    assert ok is True
    assert isinstance(info, dict)
    _assert_meve_dict(info, infile.name)


def test_verify_meve_rejects_invalid_issuer(tmp_path):
    """Modifie l’issuer pour forcer un échec."""
    infile = tmp_path / "sample.txt"
    infile.write_text("hello meve\n", encoding="utf-8")

    outfile = tmp_path / (infile.name + ".meve.json")
    generate_meve(str(infile), str(outfile), ISSUER)

    # Corruption : change l’issuer
    data = json.loads(outfile.read_text(encoding="utf-8"))
    if "raw" in data:
        data["raw"]["issuer"] = "Attacker Inc."
    else:
        data["issuer"] = "Attacker Inc."

    corrupt = tmp_path / (infile.name + ".corrupt.meve.json")
    corrupt.write_text(json.dumps(data), encoding="utf-8")

    ok, info = verify_meve(str(corrupt), expected_issuer=ISSUER)
    assert ok is False
    assert isinstance(info, (str, dict))
