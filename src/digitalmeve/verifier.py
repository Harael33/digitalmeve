from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

__all__ = ["verify_identity"]

# Required keys for a valid MEVE object (as used by the tests)
_REQUIRED_TOP = (
    "meve_version",
    "issuer",
    "timestamp",
    "metadata",
    "subject",
    "hash",
)
_REQUIRED_SUBJECT = ("filename", "size", "hash_sha256")


def _load_meve(
    obj: Union[str, Path, Dict[str, Any]]
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Load a MEVE object from a file path or directly from a dict.
    Returns (data, None) if OK, else (None, {"error": "..."}).
    """
    if isinstance(obj, (str, Path)):
        p = Path(obj)
        try:
            text = p.read_text(encoding="utf-8")
            return json.loads(text), None
        except Exception as e:  # noqa: BLE001
            return None, {"error": f"invalid file: {e.__class__.__name__}"}
    if isinstance(obj, dict):
        return obj, None
    return None, {"error": "invalid input type"}


def _missing_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return {"error": ..., "missing": [...]} if keys are missing, else {}."""
    missing = [k for k in _REQUIRED_TOP if k not in data]
    if missing:
        return {"error": "Missing required keys", "missing": missing}

    subj = data.get("subject", {})
    sub_missing = [k for k in _REQUIRED_SUBJECT if k not in subj]
    if sub_missing:
        return {"error": "Missing required keys", "missing": sub_missing}

    return {}


def verify_identity(
    meve: Union[str, Path, Dict[str, Any]],
    expected_issuer: Optional[str] = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Verify a MEVE proof.

    Returns:
      (True, data) if valid,
      (False, {"error": "...", ...}) if invalid.
    """
    data, err = _load_meve(meve)
    if err is not None:
        return False, err
    assert data is not None

    miss = _missing_keys(data)
    if miss:
        return False, miss

    # hash consistency: top-level "hash" must equal subject.hash_sha256
    top_hash = data.get("hash")
    subj_hash = data.get("subject", {}).get("hash_sha256")
    if top_hash != subj_hash:
        return False, {"error": "hash mismatch"}

    # issuer check when an expected value is provided
    if expected_issuer is not None and data.get("issuer") != expected_issuer:
        return False, {
            "error": "issuer mismatch",
            "expected": expected_issuer,
            "found": data.get("issuer"),
        }

    return True, data
