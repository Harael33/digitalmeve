import hashlib
import json
from datetime import datetime
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
import base64


# ⚡ Génération de clé (une seule fois → à externaliser plus tard)
PRIVATE_KEY = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
PUBLIC_KEY = PRIVATE_KEY.public_key()


def generate_meve(file_path: str, output_path: str = None) -> str:
    """Génère un fichier .meve (certificat numérique signé) à partir d’un fichier donné."""
    
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")
    content = file.read_bytes()

    # Hash SHA256
    file_hash = hashlib.sha256(content).hexdigest()

    # Métadonnées
    meve_data = {
        "file": file.name,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "hash": file_hash,
        "algorithm": "SHA256",
        "format": "MEVE"
    }

    # Création de la signature
    signature = PRIVATE_KEY.sign(
        json.dumps(meve_data, sort_keys=True).encode(),
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    # Encodage base64 pour stockage
    meve_data["signature"] = base64.b64encode(signature).decode()

    # Sauvegarde fichier
    if output_path is None:
        output_path = file.with_suffix(".meve")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(meve_data, f, indent=4)

    return str(output_path)


def export_public_key(path="public_key.pem"):
    """Permet d’exporter la clé publique (à distribuer pour la vérification)."""
    pem = PUBLIC_KEY.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(path, "wb") as f:
        f.write(pem)
    return path
