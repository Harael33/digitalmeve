import os, tempfile, json
from src.generator import generate_meve
from src.verifier import verify_meve

def test_verify_meve_ok_and_ko():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.txt")
        with open(file_path, "w") as f:
            f.write("hello world")

        # génération avec issuer
        meve_path = generate_meve(file_path, issuer="UnitTest", status="Pro")

        # vérif OK
        result_ok = verify_meve(file_path, meve_path)
        assert result_ok["valid"]
        assert result_ok["issuer"] == "UnitTest"

        # vérif KO avec fichier modifié
        with open(file_path, "w") as f:
            f.write("fake content")
        result_ko = verify_meve(file_path, meve_path)
        assert not result_ko["valid"]

def test_read_meve_info_minimal_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "data.bin")
        with open(file_path, "wb") as f:
            f.write(b"binarycontent")

        meve_path = generate_meve(file_path, issuer="TestIssuer", status="Personal")

        meve = json.loads(open(meve_path, encoding="utf-8").read())
        assert "issuer" in meve
        assert "hash_sha256" in meve
        assert meve["issuer"] == "TestIssuer"
