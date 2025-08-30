from __future__ import annotations
from pathlib import Path
from typing import Optional, Union


def format_identity(value: Optional[Union[str, Path]]) -> str:
    """
    - str -> retourne la string telle quelle
    - Path -> nom de fichier (sans extension) en upper()
    - None ou autres -> AttributeError
    """
    if isinstance(value, Path):
        return value.stem.upper()
    if isinstance(value, str):
        return value  # <= on ne modifie pas, pour que "ABC123" == "ABC123"
    raise AttributeError("invalid identity")
