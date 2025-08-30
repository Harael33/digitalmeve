from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple, Union


def verify_identity(identity: str) -> bool:
    """
    Identité simple : alphanumérique 3..64.
    Suffisant pour les tests (ex: 'ABC123' -> True).
    """
    return bool(re.fullmatch(r"[A-Za-z0-9]{3,64}", identity or ""))


def _load_candidate(candidate: Union[str, Path, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(candidate, (str, Path)):
        p = Path(candidate)
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    if isinstance(candidate, dict):
        return candidate
    raise TypeError("unsupported MEVE input type")


def _missing_keys(d: Dict[str, Any], keys: Iterable[str]) -> list[str]:
    return [k for k in keys if k not in d]


def verify_meve(
    candidate: Union[str, Path, Dict[str, Any]],
    *,
    expected_issuer: str | None = None,
) -> Tuple[bool, Dict[str, Any] | str]:
    """
    Retourne (ok, info)
    - ok=True  -> info est le dict MEVE validé
    - ok=False -> info est un dict avec une clé 'error' (et éventuellement 'missing')
    """
    meve = _load_candidate(candidate)

    required = ["issuer", "meve_version", "subject", "hash", "metadata", "timestamp", "preview_b64"]
    missing = _missing_keys(meve, required)
    if missing:
        return False, {"error": "Missing required keys", "missing": missing}

    subj = meve.get("subject", {})
    if not isinstance(subj, dict) or _missing_keys(subj, ["filename", "size", "hash_sha256"]):
        return False, {"error": "Missing required keys in subject"}

    if expected_issuer is not None and meve.get("issuer") != expected_issuer:
        return False, {"error": "issuer mismatch", "expected": expected_issuer, "got": meve.get("issuer")}

    # cohérence minimale : 'hash' racine == 'hash_sha256' du sujet
    if meve.get("hash") != subj.get("hash_sha256"):
        return False, {"error": "hash mismatch"}

    return True, meve
