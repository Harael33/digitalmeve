"""
DigitalMeve package init.
Expose la version et les APIs publiques de base.
"""

__version__ = "0.1.4"   # aligne ceci avec ta prochaine release/tag

from .generator import generate_meve, save_meve
from .verifier  import verify_meve

__all__ = [
    "__version__",
    "generate_meve",
    "save_meve",
    "verify_meve",
]
