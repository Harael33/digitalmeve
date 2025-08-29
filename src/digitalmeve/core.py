# src/digitalmeve/core.py
from __future__ import annotations

import base64
import datetime as _dt
import hashlib
import json
import mimetypes
import os
from typing import Dict, Tuple, Any


_MEVE_SPEC_VERSION = "1.0"


def _now_iso_utc() -> str:
    """Return an ISO-8601 timestamp in UTC without microseconds, ending with 'Z'."""
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_file_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


def _guess_mime(path: str) -> str:
    mime, _ = mimetypes.guess_type(path)
    return mime or "application/octet-stream"


def generate_meve(infile: str, outfile: str, issuer: str) -> str:
    """
    Crée un fichier de preuve (.meve JSON) pour `infile` et l’écrit dans `outfile`.

    Retourne:
        str: le chemin `outfile` (conforme à ce qu’attendent les tests qui font
             os.path.getsize(generate_meve(...)) ).
    """
    # Lecture et hachage
    raw = _read_file_bytes(infile)
    sha256 = _sha256_bytes(raw)

    # Pour inspection humaine, on met une mini preview encodée base64 (max 256 octets)
    preview = base64.b64encode(raw[:256]).decode("ascii")

    proof: Dict[str, Any] = {
        "created_at": _now_iso_utc(),
        "issuer": issuer,
        "meve_version": _MEVE_SPEC_VERSION,
        "subject": {
            "filename": os.path.basename(infile),
            "size": len(raw),
            "mime": _guess_mime(infile),
            "sha256": sha256,
            "preview_b64": preview,
        },
    }

    # Écriture de la preuve
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(proof, f, ensure_ascii=False, indent=2)

    # ⚠️ Important pour nos tests/CI: on retourne le chemin du fichier, pas le dict.
    return outfile


def verify_meve(meve_file: str, expected_issuer: str | None = None) -> Tuple[bool, Dict[str, Any]]:
    """
    Vérifie un fichier .meve et retourne (ok, info_dict).

    - ok: bool succès/échec
    - info_dict:
        - en succès: le contenu JSON complet + quelques infos calculées
        - en échec: {"error": "..."} (toujours un dict pour satisfaire les tests)
    """
    try:
        with open(meve_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Champs requis minimaux (les tests vérifient la présence de 'issuer')
        required = ["created_at", "issuer", "meve_version", "subject"]
        for k in required:
            if k not in data:
                raise KeyError(k)

        subject = data["subject"]
        for k in ["filename", "size", "mime", "sha256"]:
            if k not in subject:
                raise KeyError(k)

        if expected_issuer is not None and data.get("issuer") != expected_issuer:
            return False, {"error": f"Issuer mismatch: expected '{expected_issuer}', got '{data.get('issuer')}'"}

        # Tout est OK
        return True, {
            "message": f"Valid MEVE for '{subject.get('filename')}' at {data.get('created_at')}",
            "issuer": data.get("issuer"),
            "meve_version": data.get("meve_version"),
            "subject": subject,
            "raw": data,
        }

    except KeyError as e:
        # Les tests attendent qu'on renvoie un dict (pas une string)
        return False, {"error": f"Missing required field: KeyError('{e.args[0]}')"}
    except json.JSONDecodeError as e:
        return False, {"error": f"Invalid JSON: {e}"}
    except FileNotFoundError:
        return False, {"error": f"File not found: {meve_file}"}
    except Exception as e:
        return False, {"error": f"Unexpected error: {type(e).__name__}: {e}"}
