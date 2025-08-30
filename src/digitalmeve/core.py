from __future__ import annotations

from .utils import verify_signature


def verify_meve(public_key, data, signature) -> bool:
    return verify_signature(
        public_key,
        data,
        signature,
        algorithm='SHA256',
        strict=True,
        allow_legacy=False,
    )


def generate_meve(...):
    # ton implémentation ici
    ...
