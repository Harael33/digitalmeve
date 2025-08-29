from __future__ import annotations

import base64
import hashlib
import json
import mimetypes
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Dict, Tuple, Union


def _sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


def _now_iso() -> str:
    return (
        datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def generate_meve(
    infile: Union[str, Path],
    outdir: Union[str, Path, None] = None,
    issuer: str = "DigitalMeve Test Suite",
) -> Dict[str, Any]:
    in_path = Path(infile)
    data = _read_bytes(in_path)

    mime, _ = mimetypes.guess_type(in_path.name)
    mime = mime or "application/octet-stream"

    meve: Dict[str, Any] = {
        "message": f"Valid MEVE for '{in_path.name}' at {_now_iso()}",
        "issuer": issuer,
        "meve_version": "1.0",
        "subject": {
            "filename": in_path.name,
            "size": len(data),
            "mime": mime,
            "sha256": _sha256_bytes(data),
        },
        "preview_b64": base64.b64encode(data[:64]).decode("ascii"),
        "created_at": _now_iso(),
    }

    out_dir = Path(outdir) if outdir is not None else in_path.parent
    out_file = out_dir / f"{in_path.name}.meve.json"
    out_file.write_text(json.dumps(meve, ensure_ascii=False, indent=2))
    return meve


def verify_meve(
    meve_file_or_dict: Union[str, Path, Dict[str, Any]],
    expected_issuer: Union[str, None] = None,
) -> Tuple[bool, Dict[str, Any]]:
    if isinstance(meve_file_or_dict, (str, Path)):
        path = Path(meve_file_or_dict)
        try:
            payload: Dict[str, Any] = json.loads(path.read_text())
        except Exception as exc:  # pragma: no cover
            return False, {"error": f"invalid JSON: {exc}"}
    else:
        payload = dict(meve_file_or_dict)

    required_top = {"issuer", "meve_version", "subject", "created_at", "message"}
    missing = [k for k in required_top if k not in payload]
    if missing:
        return False, {"error": f"Missing required field: {missing[0]}"}

    if expected_issuer and payload.get("issuer") != expected_issuer:
        return False, {
            "error": "issuer mismatch",
            "got": payload.get("issuer"),
        }

    subject = payload.get("subject", {})
    required_subject = {"filename", "size", "mime", "sha256"}
    miss_sub = [k for k in required_subject if k not in subject]
    if miss_sub:
        return False, {"error": f"Missing subject field: {miss_sub[0]}"}

    return True, payload
