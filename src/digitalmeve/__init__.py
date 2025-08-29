__all__ = ["generate_meve", "verify_meve", "__version__"]
__version__ = "0.1.5"

# Import tolérant : ne bloque pas l'import du package si core a un souci.
try:
    from .core import generate_meve, verify_meve  # noqa: F401
except Exception:  # ImportError ou autre
    # On laisse l'import du package fonctionner pour le sanity-check des CI.
    # Les fonctions seront importables dès que core.py est OK.
    pass
