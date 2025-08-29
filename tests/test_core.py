import os
from pathlib import Path
from digitalmeve.core import generate_meve, verify_meve

def test_generate_meve(tmp_path: Path):
    # Arrange
    infile = tmp_path / "sample.txt"
    infile.write_text("Hello DigitalMeve", encoding="utf-8")
    outfile = tmp_path / (infile.name + ".meve")
    issuer = "DigitalMeve Test Suite"

    # Act
    meve_path = generate_meve(infile=str(infile), outfile=str(outfile), issuer=issuer)

    # Assert
    assert os.path.exists(meve_path)
    ok, info = verify_meve(meve_file=str(meve_path), expected_issuer=issuer)
    assert ok is True
    assert isinstance(info, dict)
    assert info.get("issuer") == issuer

def test_verify_meve_rejects_invalid(tmp_path: Path):
    # Arrange: .meve invalide
    fake = tmp_path / "fake.meve"
    fake.write_text("{}", encoding="utf-8")

    # Act
    ok, info = verify_meve(meve_file=str(fake), expected_issuer=None)

    # Assert
    assert ok is False
    assert isinstance(info, dict)
