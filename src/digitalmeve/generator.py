from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Optional, Dict, Any
import base64
import json
import mimetypes


def generate_meve(
    file_path: Path,
    metadata: Optional[Dict[str, Any]] = None,
    encoding: str = "utf-8",
) -> Dict[str, Any]:
    """
    Génère un MEVE (Minimum Evidence Verification Envelope).

    Args:
        file_path: chemin vers le fichier.
        metadata: dictionnaire de métadonnées additionnelles.
        encoding: encodage utilisé pour la sérialisation JSON.

    Returns:
        dict contenant le MEVE.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {file_path}")

    # Lecture du fichier
    content = file_path.read_bytes()
    file_hash = sha256(content).hexdigest()

    # Déduction du type MIME
    mime_type, _ = mimetypes.guess_type(file_path.as_posix())
    mime_type = mime_type or "application/octet-stream"

    # Construction de l'enveloppe
    meve = {
        "file_name": file_path.name,
        "file_size": len(content),
        "mime_type": mime_type,
        "hash_sha256": file_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
        "preview_b64": base64.b64encode(content[:64]).decode(encoding),
    }

    return meve


if __name__ == "__main__":
    # Exemple d'utilisation pour debug
    sample = generate_meve(Path("README.md"), metadata={"author": "test"})
    print(json.dumps(sample, indent=2))
