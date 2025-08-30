# src/digitalmeve/core.py

from __future__ import annotations  # doit absolument être en 1ère ligne

import datetime
from typing import Any, Dict

from .generator import generate_meve, verify_meve


def get_current_time() -> datetime.datetime:
    """Retourne l'heure UTC actuelle."""
    return datetime.datetime.now(datetime.timezone.utc)


def generate_meve_data(issuer: str, message: str) -> Dict[str, Any]:
    """
    Génère un dictionnaire MEVE valide en utilisant generate_meve().
    """
    return generate_meve(issuer=issuer, message=message)


def verify_meve_data(meve: Dict[str, Any]) -> Dict[str, Any]:
    """
    Vérifie la validité d'un dictionnaire MEVE en utilisant verify_meve().
    """
    return verify_meve(meve)
