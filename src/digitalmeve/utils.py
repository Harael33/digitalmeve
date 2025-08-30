from __future__ import annotations

from pathlib import Path
from typing import Any, Optional


def _pick_identity(d: dict[str, Any]) -> Optional[str]:
    """
    Récupère une identité depuis plusieurs clés possibles.
    """
    for key in ("identity", "id", "name"):
        v = d.get(key)
        if isinstance(v, str) and v.strip():
            return v
    return None


def format_identity(value: Any) -> Optional[str]:
    """
    Normalise une identité en chaîne MAJUSCULES.

    - str  -> renvoie value.upper()
    - dict -> tente 'identity' / 'id' / 'name' puis upper()
    - Path -> nom du fichier (sans extension) en upper()
    - sinon -> None
    """
    # str
    if isinstance(value, str):
        return value.upper()

    # dict-like
    if isinstance(value, dict):
        picked = _pick_identity(value)
        return picked.upper() if picked else None

    # pathlib.Path
    if isinstance(value, Path):
        return value.stem.upper()

    # type non géré
    return None
