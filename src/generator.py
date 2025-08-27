import os
import json
import hashlib
from datetime import datetime, timezone


def generate_meve(document_path: str, issuer: str | None = None, output_path: str | None = None) -> str:
    """
    Génère un fichier .MEVE (Memory Verified) à partir d’un document.
    
    Args:
        document_path (str): chemin du document d’entrée.
        issuer (str, optional): identifiant de l’émetteur (email, nom, etc.).
        output_path (str, optional): chemin de sortie du fichier .meve.json.
    
    Returns:
        str: chemin du fichier généré.
    """

    # Lire le document
    with open(document_path, "rb") as f:
        content = f.read()

    # Calcul du hash SHA-256
    doc_hash_hex = hashlib.sha256(content).hexdigest()

    # Métadonnées de base
    meta = {
        "filename": os.path.basename(document_path),
        "size": len(content),
    }

    # Timestamp UTC
    timestamp_utc = datetime.now(timezone.utc).isoformat()

    # ID court (les 8 premiers caractères du hash)
    short_id = doc_hash_hex[:8]

    # Construire l’objet MEVE
    meve = {
        "MEVE": "1",
        "Time": timestamp_utc,
        "Hash-SHA256": doc_hash_hex,
        "Meta": meta,
        "ID": short_id,
    }

    # ✅ Ajouter l’issuer si fourni
    if issuer:
        meve["Issuer"] = issuer

    # Déterminer le chemin de sortie
    if output_path is None:
        output_path = document_path + ".meve.json"

    # Sauvegarder en JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(meve, f, indent=2, ensure_ascii=False)

    return output_path
