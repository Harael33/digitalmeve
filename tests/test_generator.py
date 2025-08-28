import os
import tempfile
from digitalmeve.generator import generate_meve

def test_generate_meve_returns_dict():
    # créer un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"hello world")
        tmp_path = tmp.name

    try:
        result = generate_meve(tmp_path, issuer="tester")
        assert isinstance(result, dict)
        assert result["issuer"] == "tester"
        assert "hash" in result
        assert "mime" in result
    finally:
        os.remove(tmp_path)
