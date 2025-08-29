import json
from digitalmeve.core import generate_meve

def test_generate_and_verify_valid(tmp_path):
    # Crée un fichier de test
    sample = tmp_path / "sample.txt"
    sample.write_text("hello world")

    # Appelle generate_meve → renvoie un chemin de fichier
    outfile = generate_meve(sample)

    # Corrige : on charge le fichier JSON pour obtenir un dict
    with open(outfile, "r", encoding="utf-8") as f:
        meve = json.load(f)

    # Tests
    assert isinstance(meve, dict)
    assert "created_at" in meve
    assert "issuer" in meve
