from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union


_REQUIRED_TOP = ("meve_version", "issuer", "timestamp", "metadata", "subject", "hash")
_REQUIRED_SUBJECT = ("filename", "size", "hash_sha256")


def _load_meve(obj: Union[str, Path, Dict[str, Any]]) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Charge un objet MEVE depuis un chemin fichier (str/Path) ou retourne le dict tel quel.
    En cas d'erreur, retourne (None, {"error": "...", ...}).
    """
    if isinstance(obj, (str, Path)):
        p = Path(obj)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return data, None
        except Exception as e:
            return None, {"error": f"invalid file: {e.__class__.__name__}"}
    elif isinstance(obj, dict):
        return obj, None
    else:
        return None, {"error": "invalid input type"}


def _missing_keys(data: Dict[str, Any]) -> Dict[str, Any]:
    missing = [k for k in _REQUIRED_TOP if k not in data]
    if missing:
        # Message exact attendu par les tests : "Missing required keys"
        return {"error": "Missing required keys", "missing": missing}
    subj = data.get("subject", {})
    sub_missing = [k for k in _REQUIRED_SUBJECT if k not in subj]
    if sub_missing:
        return {"error": "Missing required keys", "missing": sub_missing}
    return {}


def verify_meve(
    meve: Union[str, Path, Dict[str, Any]],
    expected_issuer: Optional[str] = None,
) -> Tuple[bool, Dict[str, Any]]:
    """
    Vérifie une preuve MEVE.

    Retourne:
      - (True, info_dict) si valide
      - (False, {"error": "...", ...}) si invalide
    """
    data, err = _load_meve(meve)
    if err is not None:
        return False, err
    assert data is not None

    # 1) Clés requises
    miss = _missing_keys(data)
    if miss:
        return False, miss

    # 2) Cohérence hash top-level vs subject.hash_sha256
    if data.get("hash") != data.get("subject", {}).get("hash_sha256"):
        return False, {"error": "hash mismatch"}

    # 3) Issuer attendu (si demandé)
    if expected_issuer is not None and data.get("issuer") != expected_issuer:
        return False, {"error": "issuer mismatch", "expected": expected_issuer, "found": data.get("issuer")}

    # Si tout va bien, on retourne (True, data) pour que les tests puissent inspecter
    return True, data
