from __future__ import annotations

__all__ = ["generate_meve", "verify_identity", "verify_file", "__version__"]

# Aligne la version avec le badge/tests (mets la même que dans pyproject si tu publies)
__version__ = "0.1.4"

from .generator import generate_meve  # noqa: E402
from .verifier import verify_identity, verify_file  # noqa: E402
