# src/digitalmeve/core.py
from __future__ import annotations

import hashlib
import json
import mimetypes
import os
from datetime import datetime, timezone
from typing import Any, Dict, Tuple, Optional


def _utc_now_iso() -> str:
    # Timestamp ISO 8601 UTC sans microsecondes, suffixé "Z"
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_meve(infile: str, outfile: str, issuer: str) -> Dict[str, Any]:
    """
    Crée la preuve MEVE d'un fichier et l'écrit en JSON dans `outfile`.
    Retourne un dict (pas une chaîne).
    """
    if not os.path.exists(infile):
        raise FileNotFoundError(infile)
    if not issuer:
        raise ValueError("issuer must be provided")

    sha256 = _sha256_file(infile)
    size = os.path.getsize(infile)
    mime, _ = mimetypes.guess_type(infile)
    mime = mime or "application/octet-stream"

    proof: Dict[str, Any] = {
        "meve_version": "1.0",
        "created_at": _utc_now_iso(),
        "issuer": issuer,
        "subject": {
            "filename": os.path.basename(infile),
            "bytes": size,
            "mime": mime,
            "sha256": sha256,
        },
    }

    # Écrit la preuve au format JSON
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(proof, f, ensure_ascii=False, indent=2)

    return proof


def verify_meve(meve_file: str, expected_issuer: Optional[str] = None) -> Tuple[bool, Dict[str, Any]]:
    """
    Vérifie une preuve MEVE (fichier JSON).
    Retourne (ok: bool, info: dict). En cas d’erreur de structure,
    ok=False et info["error"] contient un message clair.
    """
    try:
        with open(meve_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Champs obligatoires
        issuer = data["issuer"]                     # peut lever KeyError('issuer')
        subject = data["subject"]                   # peut lever KeyError('subject')
        _ = subject["sha256"]                       # peut lever KeyError('sha256')

        # Vérification d'émetteur attendu (si fourni)
        if expected_issuer is not None and issuer != expected_issuer:
            return False, {
                "error": "issuer_mismatch",
                "issuer": issuer,
                "expected_issuer": expected_issuer,
            }

        return True, data

    except KeyError as e:
        # Format qui colle à tes tests : "Missing required field: KeyError('issuer')"
        return False, {"error": f"Missing required field: {repr(e)}"}
    except FileNotFoundError:
        return False, {"error": f"File not found: {meve_file}"}
    except json.JSONDecodeError as e:
        return False, {"error": f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return False, {"error": f"Unexpected error: {str(e)}"}
