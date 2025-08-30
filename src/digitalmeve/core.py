# Ancienne ligne trop longue (exemple fictif)
result = verify_signature(public_key, data, signature, algorithm="SHA256", strict=True, allow_legacy=False)

# Correction : couper avec parenthèses
result = verify_signature(
    public_key,
    data,
    signature,
    algorithm="SHA256",
    strict=True,
    allow_legacy=False,
)
