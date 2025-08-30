from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Dict, Optional, Any, Union


def _file_sha256(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_meve(
    file_path: Union[str, Path],
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Génère un mini 'MEVE' (structure dict) utilisé par les tests.
    Clés attendues par les tests: file_name, file_size, hash_sha256, metadata, issuer.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    content_hash = _file_sha256(path)

    return {
        "file_name": path.name,
        "file_size": path.stat().st_size,
        "hash_sha256": content_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
        # valeur par défaut exigée par les tests
        "issuer": "Personal",
    }
