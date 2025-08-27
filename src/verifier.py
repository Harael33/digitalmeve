import json
import hashlib
import os


def verify_meve(document_path: str, meve_path: str) -> bool:
    """
    Vérifie l’authenticité d’un document en comparant son hash avec un fichier .MEVE.

    Args:
        document_path (str): chemin du document original.
        meve_path (str): chemin du fichier .meve.json correspondant.

    Returns:
        bool: True si le document correspond au .MEVE, False sinon.
    """

    # Lire le document original
    with open(document_path, "rb") as f:
        content = f.read()

    doc_hash_hex = hashlib.sha256(content).hexdigest()

    # Charger le .MEVE
    with open(meve_path, "r", encoding="utf-8") as f:
        meve_data = json.load(f)

    expected_hash = meve_data.get("Hash-SHA256")

    # Comparaison stricte
    if expected_hash == doc_hash_hex:
        return True
    else:
        return False


def read_meve_info(meve_path: str) -> dict:
    """
    Lit et retourne les informations d’un fichier .MEVE.

    Args:
        meve_path (str): chemin du fichier .meve.json

    Returns:
        dict: contenu JSON du MEVE
    """

    if not os.path.exists(meve_path):
        raise FileNotFoundError(f"MEVE file not found: {meve_path}")

    with open(meve_path, "r", encoding="utf-8") as f:
        return json.load(f)
