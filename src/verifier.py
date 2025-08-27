from typing import Tuple, Dict
from .utils import sha256_file, load_json

def verify_meve(input_path: str, meve_path: str) -> Tuple[bool, Dict]:
    """
    Vérifie qu'un document correspond à sa preuve .meve.
    Retourne (ok, infos).
    """
    meve = load_json(meve_path)
    actual = sha256_file(input_path)
    expected = meve.get("hash_sha256")

    ok = (actual == expected)
    info = {
        "ok": ok,
        "expected": expected,
        "actual": actual,
        "status": meve.get("status"),
        "issuer": meve.get("issuer"),
        "spec": meve.get("spec"),
        "id": meve.get("id"),
        "time": meve.get("time"),
    }
    return ok, info
