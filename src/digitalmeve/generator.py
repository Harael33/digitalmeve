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
    *,
    outdir: Optional[Union[str, Path]] = None,
    issuer: str = "Personal",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Génère un dict MEVE minimal et, si outdir est fourni, écrit <filename>.meve.json.

    Clés requises par la suite de tests :
      - meve_version, issuer, subject{ filename,size,hash_sha256 }, timestamp, metadata
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    content_hash = _file_sha256(path)

    meve: Dict[str, Any] = {
        "meve_version": "1.0",
        "issuer": issuer,
        "subject": {
            "filename": path.name,
            "size": path.stat().st_size,
            "hash_sha256": content_hash,
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
    }

    if outdir is not None:
        od = Path(outdir)
        od.mkdir(parents=True, exist_ok=True)
        out_file = od / f"{path.name}.meve.json"
        out_file.write_text(json.dumps(meve, ensure_ascii=False, indent=2))

    return meve
