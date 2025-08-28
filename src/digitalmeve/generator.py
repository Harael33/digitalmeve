from __future__ import annotations
import os
from .utils import sha256_path, iso8601_now, guess_mime, format_identity


def generate_meve(path: str, issuer: dict) -> dict:
    """
    Génère un petit 'proof' .meve (objet Python) pour le fichier `path`.
    Ne touche pas au disque pour simplifier les tests.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    proof = {
        "file": os.path.basename(path),
        "hash": sha256_path(path),
        "mime": guess_mime(path),
        "timestamp": iso8601_now(),
        "issuer": format_identity(issuer),
        "version": "0.1",
    }
    return proof
