from __future__ import annotations

import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime, timezone


def sha256_path(path: str | Path) -> str:
    """Return the hex SHA-256 digest of a file."""
    p = Path(path)
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iso8601_now() -> str:
    """UTC timestamp in strict ISO-8601 format (Z suffix)."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def guess_mime(path: str | Path) -> str:
    """Best-effort MIME type for a path."""
    m, _ = mimetypes.guess_type(str(path))
    return m or "application/octet-stream"


def format_identity(identity: str) -> str:
    """Normalize an issuer identity for stable comparisons."""
    return identity.strip().lower()
