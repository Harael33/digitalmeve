import hashlib
import uuid

def compute_hash(data: bytes) -> str:
    """
    Retourne le hash SHA-256 en hexadécimal du contenu.
    """
    return hashlib.sha256(data).hexdigest()

def generate_id() -> str:
    """
    Génère un identifiant unique court.
    """
    return str(uuid.uuid4())[:8]
