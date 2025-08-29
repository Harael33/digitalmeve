"""
DigitalMeve - API publique
"""

from .core import generate_meve, verify_meve  # noqa: F401

__all__ = ["generate_meve", "verify_meve"]

# Pense à tenir sync avec tests/test_version.py
__version__ = "1.6.0"
