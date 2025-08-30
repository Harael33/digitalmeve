from __future__ import annotations

from pathlib import Path
from typing import Optional, Union


def format_identity(value: Optional[Union[str, Path, dict]]) -> str:
    """
    - str  -> retourne la chaîne telle quelle
    - Path -> nom du fichier (sans extension) en MAJUSCULES
    - dict -> utilise la clé 'identity' si présente
    - None/autres -> lève AttributeError
    """
    if isinstance(value, Path):
        return value.stem.upper()
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and "identity" in value:
        return str(value["identity"])
    raise AttributeError("invalid identity")
