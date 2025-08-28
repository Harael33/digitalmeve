from __future__ import annotations

from pathlib import Path
from .utils import sha256_path, iso8601_now, guess_mime, format_identity


def generate_meve(file_path: str | Path, issuer: str, signature: str | None = None) -> dict:
    """
    Create a minimal .meve-proof payload for a file.
    (This is an in-memory dict used by tests; writing to disk is up to the CLI.)
    """
    p = Path(file_path)
    return {
        "spec": "MEVE/1",
        "file_name": p.name,
        "mime": guess_mime(p),
        "sha256": sha256_path(p),
        "issued_at": iso8601_now(),
        "issuer": format_identity(issuer),
        "signature": signature or "",
    }
