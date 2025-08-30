from __future__ import annotations

import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Optional, Union


def _file_sha256(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_meve(
    file_path: Union[str, Path],
    metadata: Optional[Dict[str, Any]] = None,
    *,
    outdir: Optional[Union[str, Path]] = None,
    issuer: str = "Personal",
) -> Dict[str, Any]:
    """
    Génère un mini MEVE (dict) utilisé par la suite de tests.

    Clés attendues par les tests :
    - file_name, file_size, hash_sha256, metadata, issuer, meve_version, timestamp

    Si `outdir` est fourni, écrit un fichier JSON à côté :
    <nom_fichier>.meve.json
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    meve: Dict[str, Any] = {
        "file_name": path.name,
        "file_size": path.stat().st_size,
        "hash_sha256": _file_sha256(path),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
        "issuer": issuer,
        "meve_version": "1.0",
    }

    if outdir is not None:
        outp = Path(outdir)
        outp.mkdir(parents=True, exist_ok=True)
        json_path = outp / f"{path.name}.meve.json"
        json_path.write_text(json.dumps(meve, ensure_ascii=False, indent=2))

    return meve
