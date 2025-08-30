"""Generation helpers for DigitalMEVE.

Ce module fournit une fine couche de compatibilité autour des fonctions
de `core`. On évite les imports circulaires en n’important que les
symboles nécessaires depuis `core`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Union

# Import strict et local pour éviter tout import circulaire
from .core import generate_meve as _core_generate_meve


Pathish = Union[str, Path]


def generate_meve(
    path: Pathish,
    *,
    issuer: str = "tester",
    outdir: Path | None = None,
    return_dict: bool = True,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Génère un MEVE pour `path` via le cœur de librairie.

    Cette fonction est un simple proxy qui maintient la compatibilité
    d’import `from digitalmeve.generator import generate_meve`.

    Args:
        path: Chemin du fichier cible.
        issuer: Nom de l’émetteur à inclure dans le MEVE.
        outdir: Dossier de sortie où écrire le JSON (optionnel).
        return_dict: Si True, retourne le dict Python (par défaut).
        **kwargs: Paramètres additionnels passés au cœur.

    Returns:
        Le dictionnaire MEVE généré.
    """
    # Délègue tout au cœur avec des mots-clés explicites (lignes courtes)
    return _core_generate_meve(
        path=path,
        issuer=issuer,
        outdir=outdir,
        return_dict=return_dict,
        **kwargs,
    )
