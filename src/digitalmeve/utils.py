def format_identity(identity: dict) -> str:
    """
    Format an identity dictionary into a human-readable string.

    Args:
        identity (dict): Identity data.

    Returns:
        str: Formatted identity string.
    """
    return f"{identity.get('name')} <{identity.get('email')}>"
