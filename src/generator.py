import os
import time
import uuid
from typing import Tuple, Dict

from .utils import sha256_file, save_json

def generate_meve(input_path: str,
                  issuer: str = "personal",
                  status: str = "Personal") -> Tuple[str, Dict]:
    """
    Crée un fichier .meve JSON à côté du document source.
    Retourne (chemin_meve, dict_contenu).
    """
    if not os.path.isfile(input_path):
        raise FileNotFoundError(input_path)

    file_hash = sha256_file(input_path)
    meta = {
        "original_name": os.path.basename(input_path),
        "size": os.path.getsize(input_path),
    }

    meve = {
        "spec": "MEVE/1",
        "status": status,             # Personal | Pro | Official
        "issuer": issuer,             # ex: email ou domaine plus tard
        "time": int(time.time()),     # epoch UTC
        "hash_sha256": file_hash,
        "id": uuid.uuid4().hex[:12],  # identifiant court
        "signature": None,            # placeholder (Ed25519 à venir)
        "meta": meta,
    }

    out_path = f"{input_path}.meve"
    save_json(out_path, meve)
    return out_path, meve
