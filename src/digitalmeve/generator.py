from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Union

from .core import generate_meve as _gen


def generate(
    infile: Union[str, Path], outdir: Union[str, Path, None] = None
) -> Dict[str, Any]:
    """
    Petit wrapper conservé pour compatibilité interne.
    """
    return _gen(infile=infile, outdir=outdir)
