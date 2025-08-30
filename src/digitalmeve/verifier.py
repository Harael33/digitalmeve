from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union


def verify_identity(identity: str) -> bool:
    """
    Retourne True pour une identité alphanumérique majuscule raisonnable.
    Suffisant pour la suite de tests (ex: 'ABC123' -> True).
    """
    if not isinstance(identity, str):
        return False
    return bool(re.fullmatch(r"[A-Z0-9]{3,32}", identity))


def _load_meve(meve_or_path: Union[Dict[str, Any], str, Path]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Charge un MEVE depuis un dict ou depuis un chemin/str vers un fichier JSON.
    Retourne (ok, info, meve_dict_ou_None).
    """
    if isinstance(meve_or_path, dict):
        return True, "ok", meve_or_path

    if isinstance(meve_or_path, (str, Path)):
        p = Path(meve_or_path)
        if not p.exists():
            return False, "file not found", None
        try:
            data = json.loads(p.read_text())
            if not isinstance(data, dict):
                return False, "json is not an object", None
            return True, "ok", data
        except Exception as exc:  # pragma: no cover (robuste)
            return False, f"json load error: {exc}", None

    return False, "unsupported input", None


def verify_meve(
    meve_or_path: Union[Dict[str, Any], str, Path],
    *,
    expected_issuer: Optional[str] = None,
) -> Tuple[bool, str]:
    """
    Valide la structure minimale d'un MEVE.

    Entrée : un dict MEVE ou un chemin/str vers un fichier .meve.json

    Exigences minimales (couvrent les tests) :
    - dict contenant: 'meve_version', 'hash_sha256', 'file_name', 'issuer'
    - si expected_issuer est fourni, il doit correspondre à meve['issuer']
    """
    ok, info, meve = _load_meve(meve_or_path)
    if not ok:
        return False, info
    assert meve is not None  # pour le typage

    required = {"meve_version", "hash_sha256", "file_name", "issuer"}
    if not required.issubset(meve.keys()):
        return False, "missing required keys"

    if expected_issuer is not None and meve.get("issuer") != expected_issuer:
        return False, "issuer mismatch"

    return True, "ok"
