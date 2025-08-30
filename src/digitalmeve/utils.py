from __future__ import annotations

from pathlib import Path
from typing import Optional, Union


def format_identity(value: Optional[Union[str, Path]]) -> str:
    """
    - str -> upper()
    - Path -> nom de fichier (sans extension) en upper()
    - autres / None -> lève AttributeError (comme le test l’attend)
    """
    if isinstance(value, Path):
        return value.stem.upper()
    if isinstance(value, str):
        return value.upper()
    raise AttributeError("invalid identity")
