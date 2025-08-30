from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Union

from .core import generate_meve as _core_generate_meve


def generate_meve(
    file_path: Union[str, Path],
    issuer: str = "tester",
    meve_version: str = "1.0",
) -> Dict[str, Any]:
    """
    Public wrapper for the core.generate_meve function.

    Args:
        file_path: Path to the file to be converted into MEVE.
        issuer: The identity of the issuer creating the MEVE file.
        meve_version: Version string for MEVE format.

    Returns:
        A dictionary containing the MEVE metadata.
    """
    return _core_generate_meve(file_path, issuer=issuer, meve_version=meve_version)
