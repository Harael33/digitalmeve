from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Dict, Any

from .utils import sha256_path, iso8601_now, guess_mime


def generate_meve(
    input_path: str | Path,
    issuer: Optional[str] = None,
    mime_type: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Génère la preuve .meve (en mémoire) pour un fichier donné.
    - input_path  : chemin du document d'origine
    - issuer      : identifiant de l'émetteur (email, org…, optionnel)
    - mime_type   : MIME explicite (sinon déduit)

    Retourne un dict prêt à être sérialisé en JSON.
    """
    p = Path(input_path)
    if not p.is_file():
        raise FileNotFoundError(f"Input file not found: {p}")

    proof = {
        "format": "MEVE",
        "version": "1",
        "doc": {
            "name": p.name,
            "mime": mime_type or guess_mime(p),
            "sha256": sha256_path(p),
            "size": p.stat().st_size,
        },
        "issuer": issuer,
        "generated_at": iso8601_now(),
        # "signature": "base64…"  # (optionnel si tu ajoutes une signature plus tard)
    }
    return proof


def save_meve(proof: Dict[str, Any], out_path: str | Path) -> Path:
    """
    Sauvegarde le dict
