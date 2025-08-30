from __future__ import annotations

import datetime
from typing import Any, Dict

from .generator import generate_meve, verify_meve


def get_current_time() -> datetime.datetime:
    """Retourne l'heure UTC actuelle."""
    return datetime.datetime.now(datetime.timezone.utc)


def generate_meve_data(issuer: str, message: str) -> Dict[str, Any]:
    """Génère un dictionnaire MEVE valide."""
    return generate_meve(issuer=issuer, message=message)


def verify_meve_data(meve: Dict[str, Any]) -> Dict[str, Any]:
    """Vérifie la validité d'un dictionnaire MEVE."""
    return verify_meve(meve)
