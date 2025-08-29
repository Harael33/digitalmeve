def verify_meve(*, meve_file: str, expected_issuer: str | None = None) -> tuple[bool, dict]:
    """
    Vérifie un fichier .meve et retourne (ok, infos).
    - ok = True si valide, False sinon
    - infos = dict avec les métadonnées ou les erreurs
    """
    try:
        import json
        from pathlib import Path

        path = Path(meve_file)
        data = json.loads(path.read_text(encoding="utf-8"))

        issuer = data.get("issuer")
        if not issuer:
            return False, {"error": "Missing required field: issuer"}

        if expected_issuer and issuer != expected_issuer:
            return False, {"error": "Issuer mismatch", "issuer": issuer}

        return True, data

    except Exception as e:
        return False, {"error": str(e)}
