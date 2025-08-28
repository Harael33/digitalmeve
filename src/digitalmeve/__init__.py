# src/digitalmeve/__init__.py
"""
DigitalMeve — API publique du package.
Expose les fonctions clés et la version du package.
"""

from importlib.metadata import PackageNotFoundError, version

# Version du package (tombe en 0.0.0 en environnement non installé)
try:
    __version__ = version("digitalmeve")
except PackageNotFoundError:
    __version__ = "0.0.0"

# API publique
from .generator import generate_meve
from .verifier import verify_identity
from .utils import format_identity, sha256_path, iso8601_now, guess_mime

__all__ = [
    "generate_meve",
    "verify_identity",
    "format_identity",
    "sha256_path",
    "iso8601_now",
    "guess_mime",
    "__version__",
]
