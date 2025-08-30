"""
DigitalMeve - API publique
"""
from .core import generate_meve, verify_meve  # noqa: F401

__all__ = ["generate_meve", "verify_meve"]
__version__ = "1.6.1"
