def format_identity(data: dict) -> dict:
    """
    Format une identité simple.
    Exemple : {"name": "John", "age": 30} -> {"name": "John", "age": 30}
    """
    if not isinstance(data, dict):
        raise ValueError("data doit être un dictionnaire")
    return {
        "name": data.get("name", ""),
        "age": data.get("age", None)
    }
