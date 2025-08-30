from __future__ import annotations

import base64
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


def _small_preview_b64(path: Path, limit: int = 64) -> str:
    try:
        data = path.read_bytes()[:limit]
        return base64.b64encode(data).decode("ascii")
    except Exception:
        return ""


def generate_meve(
    file_path: Union[str, Path],
    *,
    outdir: Optional[Path] = None,
    issuer: str = "Personal",
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"file not found: {path}")

    content_hash = _file_sha256(path)
    preview_b64 = _small_preview_b64(path)

    meve: Dict[str, Any] = {
        "issuer": issuer,
        "meve_version": "1.0",
        "hash": content_hash,
        "preview_b64": preview_b64,
        "metadata": metadata or {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "subject": {
            "filename": path.name,
            "size": path.stat().st_size,
            "hash_sha256": content_hash,
        },
        # champs tolérés par d'autres bouts de code
        "file_name": path.name,
        "file_size": path.stat().st_size,
    }

    if outdir:
        outdir = Path(outdir)
        outdir.mkdir(parents=True, exist_ok=True)
        out_file = outdir / f"{path.name}.meve.json"
        out_file.write_text(json.dumps(meve, ensure_ascii=False, indent=2))

    return meve
