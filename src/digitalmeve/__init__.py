"""
DigitalMeve — The Certified Digital Memory (.MEVE)

Package init: exposes version and core helpers.
"""

__all__ = ["generate_meve", "verify_meve", "__version__"]
__version__ = "1.6.0"

# Import tolérant (évite de casser l'import du package si core.py a un souci transitoire).
try:
    from .core import generate_meve, verify_meve  # noqa: F401
except Exception:
    pass
# src/digitalmeve/__init__.py
__version__ = "1.6.0"

from .core import generate_meve, verify_meve

__all__ = ["generate_meve", "verify_meve", "__version__"]
