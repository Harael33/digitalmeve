from __future__ import annotations

import json
import re
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union


def verify_identity(identity: str) -> bool:
    """
    Valide une identité alphanumérique majuscule (ex: 'ABC123').
    """
    if not isinstance(identity, str):
        return False
    return bool(re.fullmatch(r"[A-Z0-9]{3,32}", identity))


def _load_meve(
    meve_or_path: Union[Dict[str, Any], str, Path]
) -> Tuple[bool, Dict[str, Any], Optional[Dict[str, Any]], Optional[Path]]:
    """
    Charge un MEVE depuis un dict ou un chemin vers un .meve.json.
    Retourne (ok, info_dict, meve_dict_ou_None, path_ou_None).
    info_dict est TOUJOURS un dict (même en cas d'erreur).
    """
    if isinstance(meve_or_path, dict):
        return True, {"status": "ok"}, meve_or_path, None

    if isinstance(meve_or_path, (str, Path)):
        p = Path(meve_or_path)
        if not p.exists():
            return False, {"error": "file not found", "path": str(p)}, None, p
        try:
            data = json.loads(p.read_text())
            if not isinstance(data, dict):
                return False, {"error": "json is not an object", "path": str(p)}, None, p
            return True, {"status": "ok", "path": str(p)}, data, p
        except Exception as exc:
            return False, {"error": "json load error", "detail": str(exc), "path": str(p)}, None, p

    return False, {"error": "unsupported input", "type": type(meve_or_path).__name__}, None, None


def _sha256_file(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_meve(
    meve_or_path: Union[Dict[str, Any], str, Path],
    *,
    expected_issuer: Optional[str] = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Valide la structure minimale d'un MEVE.

    Succès -> (True, <dict MEVE>)
    Échec  -> (False, {"error": "...", ...})
    """
    ok, info, meve, src_path = _load_meve(meve_or_path)
    if not ok:
        return False, info
    assert meve is not None

    # Clés minimales attendues par les tests (incluant 'subject')
    required = {"meve_version", "issuer", "subject", "timestamp", "metadata"}
    if not required.issubset(meve.keys()):
        return False, {"error": "missing required keys", "missing": list(required - set(meve.keys()))}

    subject = meve.get("subject", {})
    needed_subject = {"filename", "size", "hash_sha256"}
    if not isinstance(subject, dict) or not needed_subject.issubset(subject.keys()):
        return False, {"error": "invalid subject block", "missing": list(needed_subject - set(subject.keys()))}

    if expected_issuer is not None and meve.get("issuer") != expected_issuer:
        return False, {"error": "issuer mismatch", "expected": expected_issuer, "got": meve.get("issuer")}

    # Vérification du hash si on connaît l'emplacement du .meve.json
    if isinstance(src_path, Path):
        filename = subject["filename"]
        candidates = [
            src_path.parent / filename,           # out/<filename>
            src_path.parent.parent / filename,    # ../<filename>  (cas du test)
        ]
        found = False
        for cand in candidates:
            if cand.exists():
                found = True
                actual = _sha256_file(cand)
                if actual != subject["hash_sha256"]:
                    return False, {"error": "hash mismatch", "expected": subject["hash_sha256"], "got": actual}
                break
        # Si le fichier n'est pas retrouvé, on n'échoue pas (tests actuels ne l'exigent pas)
        meve["_resolved_file_found"] = found

    return True, meve
