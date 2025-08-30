from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple, Union


def _load_meve(obj: Union[Dict[str, Any], str, Path]) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    p = Path(obj)
    data = p.read_text(encoding="utf-8")
    return json.loads(data)


def _missing_keys(d: Dict[str, Any], keys: Iterable[str]) -> list[str]:
    return [k for k in keys if k not in d]


def verify_identity(value: Any) -> bool:
    return isinstance(value, str) and len(value) > 0


def verify_meve(
    obj: Union[Dict[str, Any], str, Path],
    *,
    expected_issuer: str | None = None,
) -> Tuple[bool, Dict[str, Any] | str]:
    try:
        meve = _load_meve(obj)
    except Exception as exc:
        return False, {"error": f"invalid json: {exc}"}

    required = ["issuer", "meve_version", "subject", "metadata", "timestamp"]
    missing = _missing_keys(meve, required)
    if missing:
        # Le test cherche exactement "Missing required keys"
        return False, {"error": "Missing required keys", "missing": missing}

    if expected_issuer and meve.get("issuer") != expected_issuer:
        return False, {"error": "issuer mismatch", "expected": expected_issuer}

    return True, meve
