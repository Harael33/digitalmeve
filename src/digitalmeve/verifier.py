from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Dict, Any

from .utils import sha256_path


def verify_meve(
    meve_path: str | Path,
    original_path: Optional[str | Path] = None,
) -> Dict[str, Any]:
    """
    Vérifie une preuve .meve.
    - meve_path: chemin vers le fichier .meve (JSON)
    - original_path (optionnel): fichier original à comparer
      (si fourni, on recalcule son SHA-256 et on compare)

    Retourne un dict { ok: bool, details: {...}, reason: str|None }.
    """
    mp = Path(meve_path)
    if not mp.is_file():
        return {"ok": False, "reason": f".meve not found: {mp}", "details": {}}

    try:
        data = json.loads(mp.read_text(encoding="utf-8"))
    except Exception as e:
        return {"ok": False, "reason": f"Invalid JSON: {e}", "details": {}}

    details: Dict[str, Any] = {"meve": data}
    expected_hash = (data.get("doc") or {}).get("sha256")

    if original_path:
        op = Path(original_path)
        if not op.is_file():
            return {"ok": False, "reason": f"original not found: {op}", "details": details}
        actual_hash = sha256_path(op)
        details["recomputed_sha256"] = actual_hash
        if expected_hash and actual_hash != expected_hash:
            return {"ok": False, "reason": "hash_mismatch", "details": details}

    # Ici tu pourras ajouter des vérifs de signature, d’issuer, etc.
    return {"ok": True, "reason": None, "details": details}
