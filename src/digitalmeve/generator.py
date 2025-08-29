from __future__ import annotations

from pathlib import Path
from typing import Union, Dict, Any

from .core import generate_meve as _core_generate_meve


def generate_meve(
    infile: Union[str, Path],
    outfile: Union[str, Path, None] = None,
    issuer: str | None = None,
) -> Dict[str, Any] | str:
    """
    Mince « wrapper » autour de core.generate_meve.

    - Si `outfile` est fourni, on écrit le JSON et on retourne le chemin (str).
    - Sinon, on retourne directement le dict MEVE (comportement de core).
    """
    meve = _core_generate_meve(infile=infile, outfile=outfile, issuer=issuer)
    return str(outfile) if outfile else meve
