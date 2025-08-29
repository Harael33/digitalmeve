from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Tuple, Union, Dict, Any

__all__ = ["generate_meve", "verify_meve"]


def _sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _utc_now_isoz() -> str:
    # Compatible Python 3.10 : timezone.utc + suffixe Z
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def generate_meve(
    infile: Union[str, Path],
    outfile: Union[str, Path, None] = None,
    issuer: str | None = None,
) -> Dict[str, Any]:
    """
    Crée un objet MEVE (dict). Si `outfile` est fourni, écrit le JSON.
    """
    p = Path(infile)
    data = p.read_bytes()
    mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"

    meve: Dict[str, Any] = {
        "message": f"Valid MEVE for '{p.name}' at {_utc_now_isoz()}",
        "issuer": issuer or "DigitalMeve Test Suite",
        "meve_version": "1.0",
        "subject": {
            "filename": p.name,
            "size": len(data),
            "mime": mime,
            "sha256": _sha256_bytes(data),
        },
        "preview_b64": base64.b64encode(data[:64]).decode("ascii"),
        "raw": {
            "created_at": _utc_now_isoz(),
            "issuer": issuer or "DigitalMeve Test Suite",
            "meve_version": "1.0",
            "subject": {
                "filename": p.name,
                "size": len(data),
                "mime": mime,
                "sha256": _sha256_bytes(data),
            },
        },
    }

    if outfile:
        Path(outfile).write_text(
            json.dumps(meve, ensure_ascii=False, separators=(",", ":"))
        )

    return meve


def verify_meve(
    meve_input: Union[str, Path, Dict[str, Any]],
    expected_issuer: str | None = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Valide un MEVE. Retourne (ok, info_dict).
    - ok: bool
    - info_dict: le MEVE si valide, sinon {"error": "..."}
    """
    if isinstance(meve_input, (str, Path)):
        try:
            meve: Dict[str, Any] = json.loads(Path(meve_input).read_text())
        except Exception as e:
            return False, {"error": f"Invalid JSON: {e}"}
    else:
        meve = meve_input

    # Champs requis
    for k in ("issuer", "meve_version", "subject"):
        if k not in meve:
            return False, {"error": f"Missing required field: KeyError('{k}')"}

    if expected_issuer and meve.get("issuer") != expected_issuer:
        return False, {"error": "Issuer mismatch"}

    if not isinstance(meve.get("subject"), dict):
        return False, {"error": "Invalid subject"}

    return True, meve
