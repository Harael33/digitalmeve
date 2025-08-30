from __future__ import annotations

import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Optional, Union
import mimetypes


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
      - mime_type, top-level "hash", et compat top-level file_name / file_size
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    content_hash = _file_sha256(path)
    mime, _ = mimetypes.guess_type(path.name)
    if not mime:
        mime = "application/octet-stream"

    meve: Dict[str, Any] = {
        "meve_version": "1.0",
        "issuer": issuer,
        "subject": {
            "filename": path.name,
            "size": path.stat().st_size,
            "hash_sha256": content_hash,
        },
        # compat attendue par certains tests
        "file_name": path.name,
        "file_size": path.stat().st_size,
        "hash": content_hash,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata": metadata or {},
        "mime_type": mime,
    }

    if outdir is not None:
        od = Path(outdir)
        od.mkdir(parents=True, exist_ok=True)
        out_file = od / f"{path.name}.meve.json"
        out_file.write_text(json.dumps(meve, ensure_ascii=False, indent=2))

    return meve
