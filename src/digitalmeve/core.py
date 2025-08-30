from __future__ import annotations

from typing import Any, Dict, Optional, Union
from pathlib import Path

# On utilise les vraies implémentations du nouveau module
from . import generator as _gen


def _coerce_message(
    args: tuple,
    *,
    message: Optional[Union[str, bytes]] = None,
    infile: Optional[Union[str, Path]] = None,
) -> str:
    """
    Déduit le 'message' à partir :
      - d'un argument positionnel unique (str|bytes)
      - de message=...
      - d'un chemin infile=... (contenu lu en texte utf-8)
    """
    if message is None and args:
        maybe = args[0]
        if isinstance(maybe, bytes):
            return maybe.decode("utf-8", errors="replace")
        return str(maybe)

    if message is None and infile is not None:
        p = Path(infile)
        try:
            return p.read_text(encoding="utf-8")
        except Exception:
            # en dernier recours, on met juste le nom de fichier
            return p.name

    if isinstance(message, bytes):
        return message.decode("utf-8", errors="replace")

    return message or ""


def generate_meve(
    *args,
    issuer: Optional[str] = None,
    message: Optional[Union[str, bytes]] = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Wrapper rétro-compatible.

    Accepte encore :
      - un argument positionnel (message)
      - kwargs hérités : infile, outfile, outdir (ignorés ici)
    """
    # Extraire anciens kwargs sans échouer si présents
    infile = kwargs.pop("infile", None)
    kwargs.pop("outfile", None)  # ignoré
    kwargs.pop("outdir", None)   # ignoré

    msg = _coerce_message(args, message=message, infile=infile)
    iss = issuer or "DigitalMeve Test Suite"

    # Appel vers la nouvelle implémentation
    return _gen.generate_meve(issuer=iss, message=msg)


def verify_meve(
    meve: Dict[str, Any],
    *,
    expected_issuer: Optional[str] = None,
    **_kwargs,
) -> Dict[str, Any]:
    """
    Wrapper rétro-compatible.

    Gère encore expected_issuer=... et renvoie une erreur cohérente
    si l'émetteur ne correspond pas.
    """
    result = _gen.verify_meve(meve)

    if result.get("valid") and expected_issuer:
        if meve.get("issuer") != expected_issuer:
            return {"valid": False, "error": "Issuer mismatch"}

    return result
