import hashlib
import mimetypes
import datetime
from typing import Union

def sha256_path(path: str) -> str:
    """Calcule le SHA256 d'un fichier donné."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def iso8601_now() -> str:
    """Retourne l'heure actuelle en ISO 8601 (UTC)."""
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def guess_mime(path: str) -> str:
    """Devine le type MIME d'un fichier, ou 'application/octet-stream' par défaut."""
    mime, _ = mimetypes.guess_type(path)
    return mime or "application/octet-stream"

def format_identity(identity: Union[str, dict, None]) -> str:
    """
    Formate une identité en string normalisée.
    - None → ""
    - dict → str(dict)
    - string → strip + lower
    """
    if identity is None:
        return ""
    if not isinstance(identity, str):
        identity = str(identity)
    return identity.strip().lower()
