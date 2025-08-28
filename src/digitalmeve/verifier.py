def verify_identity(data: dict) -> bool:
    """Renvoie True si l'identité est marquée 'verified'."""
    if not isinstance(data, dict):
        return False
    return data.get("verified", False) is True
