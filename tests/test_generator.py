import json
import time
from src import utils

def generate_proof(content: bytes, issuer: str = "Unknown") -> dict:
    """
    Génère un fichier de preuve (MEVE minimal) sous forme de dictionnaire.
    """
    proof = {
        "status": "Personal",
        "issuer": issuer,
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hash": utils.compute_hash(content),
        "id": utils.generate_id()
    }
    return proof

def export_proof(proof: dict, filepath: str):
    """
    Sauvegarde la preuve dans un fichier JSON.
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(proof, f, indent=2, ensure_ascii=False)
