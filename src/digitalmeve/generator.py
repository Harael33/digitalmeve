from __future__ import annotations
from typing import List


def generate_meve(data: str) -> List[str]:
    """Generate a MEVE (Minimal Example Verifiable Entity).

    Version minimale/placeholder : retourne l'entrée en MAJUSCULES
    dans une liste, histoire de garder une signature propre et de
    satisfaire les linters (black/flake8) sans imports inutiles.
    """
    return [data.upper()]
