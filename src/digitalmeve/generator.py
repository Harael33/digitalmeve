from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Optional
import base64
import mimetypes


def generate_meve(
    file_path: Path,
    metadata: Optional[Dict[str, Any]] = None,
    encoding: str = "utf-8",
) -> Dict[str, Any]:
    """
    Génère un MEVE minimal (dictionnaire) pour un fichier.
    """
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    content = p.read_bytes()
    file_hash = sha256(content).hexdigest()
    mime_type, _ = mimetypes.guess_type(p.as_posix())
    preview_b64 = base64.b64encode(content[:64]).decode(encoding)

    return {
        "file_name": p.name,
        "file_size": len(content),
        "mime_type": mime_type or "application/octet-stream",
        "hash_sha256": file_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
        "preview_b64": preview_b64,
        # clé attendue par le test
        "issuer": "Personal",
    }
