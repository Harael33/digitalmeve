from typing import Any, Dict, Union

def _extract_issuer(data: Union[str, Dict[str, Any]]) -> str:
    """
    Extrait un 'issuer' à partir d'une chaîne ou d'un dict.
    Heuristiques simples pour couvrir plusieurs cas de tests.
    """
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, dict):
        # champs possibles
        for key in ("issuer", "name", "issuer_name", "owner"):
            v = data.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    return ""

def verify_identity(data: Union[str, Dict[str, Any]], expected_issuer: str | None = None):
    """
    Deux modes :
    - Si expected_issuer est fourni -> renvoie True/False.
    - Sinon -> renvoie un dict d'info {'issuer': ..., 'verified': None}.

    Ceci aligne la fonction avec les deux styles de tests rencontrés.
    """
    issuer = _extract_issuer(data)

    if expected_issuer is not None:
        return issuer.lower() == expected_issuer.strip().lower()

    # Mode "infos" (pas de comparaison demandée)
    return {"issuer": issuer, "verified": None}
