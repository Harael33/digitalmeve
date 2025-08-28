import hashlib
import mimetypes
from datetime import datetime
from typing import Any, Dict, Union

def sha256_path(path: str) -> str:
    """Renvoie le SHA-256 (hex) d'un fichier."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def iso8601_now() -> str:
    """Timestamp ISO-8601 UTC sans microsecondes, suffixé 'Z'."""
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def guess_mime(path: str) -> str:
    """Détecte le mime-type via l'extension (fallback 'application/octet-stream')."""
    mt, _ = mimetypes.guess_type(path)
    return mt or "application/octet-stream"

def format_identity(identity: Union[str, Dict[str, Any], None]) -> Union[str, Dict[str, Any]]:
    """
    Normalise une identité :
    - si dict -> on retourne le dict tel quel (les tests s'attendent à un dict)
    - si str  -> on trim et on renvoie la chaîne
    - si None -> chaîne vide
    - sinon   -> str(value).strip()
    """
    if isinstance(identity, dict):
        return identity
    if identity is None:
        return ""
    if isinstance(identity, str):
        return identity.strip()
    return str(identity).strip()
