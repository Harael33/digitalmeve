from __future__ import annotations
import hashlib
import mimetypes
import datetime

_CHUNK = 1024 * 1024  # 1MB


def sha256_path(path: str) -> str:
    """Calcule le SHA-256 d'un fichier (hex)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(_CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def iso8601_now() -> str:
    """Retourne l'instant courant en ISO 8601 (UTC, sans microsecondes)."""
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def guess_mime(path: str) -> str:
    """Devine le type MIME d'un fichier, défaut: application/octet-stream."""
    mime, _ = mimetypes.guess_type(path)
    return mime or "application/octet-stream"


def format_identity(data: dict) -> dict:
    """Normalise une identité simple."""
    if not isinstance(data, dict):
        raise ValueError("data doit être un dictionnaire")
    return {
        "name": data.get("name", ""),
        "email": data.get("email", ""),
        "verified": bool(data.get("verified", False)),
    }
