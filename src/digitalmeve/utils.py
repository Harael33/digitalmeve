from __future__ import annotations
from pathlib import Path
from typing import Optional, Union


def format_identity(value: Optional[Union[str, Path]]) -> str:
    """
    - str -> retourne la string telle quelle
    - Path -> retourne le nom du fichier (sans extension) en majuscules
    - None ou autres -> lève AttributeError
    """
    if isinstance(value, Path):
        return value.stem.upper()
    if isinstance(value, str):
        return value
    raise AttributeError("invalid identity")
