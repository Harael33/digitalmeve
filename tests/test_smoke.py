from pathlib import Path
import json
from digitalmeve import generate_meve, verify_meve

def test_smoke(tmp_path: Path):
    f = tmp_path / "hello.txt"
    f.write_text("bonjour")

    proof = generate_meve(f)

    meve_path = tmp_path / "hello.meve"
    meve_path.write_text(json.dumps(proof))

    result = verify_meve(meve_path, f)
    assert result["ok"] is True
