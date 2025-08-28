from __future__ import annotations

from pathlib import Path
from .utils import sha256_path, format_identity


def verify_identity(proof: dict, expected_issuer: str) -> bool:
    """Check the issuer identity recorded in a proof."""
    try:
        return format_identity(proof.get("issuer", "")) == format_identity(expected_issuer)
    except Exception:
        return False


def verify_file(file_path: str | Path, proof: dict) -> bool:
    """Check that the file's SHA-256 matches the proof."""
    try:
        return sha256_path(file_path) == proof.get("sha256")
    except Exception:
        return False
