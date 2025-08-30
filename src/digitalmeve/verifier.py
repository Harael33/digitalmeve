# Exemple avant (ligne trop longue)
if not isinstance(meve, dict) or "issuer" not in meve or "meve_version" not in meve or "subject" not in meve:
    return False, {"error": "missing required keys", "missing": ["issuer", "meve_version", "subject"]}

# ✅ Version corrigée (max 88 chars/ligne)
if (
    not isinstance(meve, dict)
    or "issuer" not in meve
    or "meve_version" not in meve
    or "subject" not in meve
):
    return False, {
        "error": "missing required keys",
        "missing": ["issuer", "meve_version", "subject"],
    }

# Exemple avant (94 > 88)
if expected_issuer and meve.get("issuer") != expected_issuer:
    return False, {"error": "issuer mismatch", "expected": expected_issuer}

# ✅ Corrigé
if expected_issuer and meve.get("issuer") != expected_issuer:
    return False, {
        "error": "issuer mismatch",
        "expected": expected_issuer,
    }

# Exemple avant (106 > 88)
return True, {"issuer": meve["issuer"], "meve_version": meve["meve_version"], "subject": meve["subject"]}

# ✅ Corrigé
return True, {
    "issuer": meve["issuer"],
    "meve_version": meve["meve_version"],
    "subject": meve["subject"],
}
