from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import base64
import json
import mimetypes


MEVE_VERSION = "1.0"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _guess_mime(filename: str) -> str:
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"


def _b64(data: bytes) -> str:
    # urlsafe + pas de '=' final pour rester compact
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _sha256_hex(data: bytes) -> str:
    return sha256(data).hexdigest()


def _make_subject(filename: str, data: bytes) -> Dict[str, Any]:
    return {
        "filename": filename,
        "size": len(data),
        "mime": _guess_mime(filename),
        "sha256": _sha256_hex(data),
    }


def _make_preview(data: bytes, max_bytes: int = 64) -> str:
    # petit aperçu base64 pour tests/débogage
    head = data[:max_bytes]
    return _b64(head) if head else ""


def generate_meve(
    data: bytes,
    *,
    filename: str = "sample.txt",
    issuer: str = "tester",
    outdir: Optional[Path] = None,
) -> Dict[str, Any]:
    """
    Génère un 'MEVE' minimal conforme aux attentes des tests.
    - retourne un dict
    - contient au moins 'hash' (sha256 du contenu)
    - écrit un fichier JSON si `outdir` est fourni (nom: <filename>.meve.json)
    """
    created_at = _utc_now_iso()
    subject = _make_subject(filename, data)
    preview_b64 = _make_preview(data)

    payload = {
        "message": f"Valid MEVE for '{filename}' at {created_at}",
        "issuer": issuer,
        "meve_version": MEVE_VERSION,
        "subject": subject,
        "preview_b64": preview_b64,
        # champ 'raw' pour garder les métadonnées brutes/signables si besoin
        "raw": {
            "created_at": created_at,
            "issuer": issuer,
            "meve_version": MEVE_VERSION,
            "subject": subject,
            "sha256": subject["sha256"],
        },
        # certains tests s’attendent explicitement à la clé 'hash'
        "hash": subject["sha256"],
    }

    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        outpath = outdir / f"{filename}.meve.json"
        # pas d'f-string “vide” -> message clair
        with outpath.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    return payload
