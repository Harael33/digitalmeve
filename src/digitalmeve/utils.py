from __future__ import annotations

import hashlib
import mimetypes
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def iso8601_now() -> str:
    """Timestamp ISO 8601 (UTC)."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    """SHA-256 hex d'un buffer mémoire."""
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha256_path(path: str | Path) -> str:
    """SHA-256 hex d'un fichier (streaming)."""
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def guess_mime(path: str | Path) -> Optional[str]:
    mime, _ = mimetypes.guess_type(str(path))
    return mime or "application/octet-stream"
