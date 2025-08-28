"""
DigitalMeve package init.
Expose la version pour setuptools (dynamic version) et les objets publics.
"""

# ⚠️ Mets ici la version courante de ton projet (aligne avec la release)
__version__ = "0.1.4"

# Si tu veux exposer des APIs au top-level:
# from .generator import generate_meve
# from .verifier import verify_meve

__all__ = ["__version__"]
