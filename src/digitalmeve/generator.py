from __future__ import annotations

import base64
import datetime
import hashlib
from typing import Any, Dict


def _utc_now_iso() -> str:
    """UTC timestamp with Z suffix."""
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def generate_meve(*, issuer: str, message: str) -> Dict[str, Any]:
    """
    Build a minimal MEVE dict with deterministic hash and preview.

    Keys produced:
      - issuer, message, timestamp, hash, meve_version, preview_b64
    """
    ts = _utc_now_iso()
    payload = f"{issuer}:{message}:{ts}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    preview_b64 = base64.b64encode(message.encode("utf-8")).decode("ascii")

    return {
        "issuer": issuer,
        "message": message,
        "timestamp": ts,
        "hash": digest,
        "meve_version": "1.0",
        "preview_b64": preview_b64,
    }


def verify_meve(meve: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a MEVE dict. Returns {'valid': True} or {'valid': False, 'error': '<reason>'}.
    """
    required = ("issuer", "message", "timestamp", "hash")
    for key in required:
        if key not in meve:
            return {"valid": False, "error": f"Missing"}
    payload = f"{meve['issuer']}:{meve['message']}:{meve['timestamp']}"
    expected = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    if expected != meve.get("hash"):
        return {"valid": False, "error": "Hash mismatch"}
    return {"valid": True}
