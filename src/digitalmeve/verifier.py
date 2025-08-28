def verify_identity(data: dict) -> bool:
    """
    Vérifie si l'identité est marquée comme vérifiée.
    Exemple : {"name": "Alice", "verified": True} -> True
    """
    if not isinstance(data, dict):
        return False
    return data.get("verified", False) is True
