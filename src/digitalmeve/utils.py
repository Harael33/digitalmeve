# src/digitalmeve/utils.py
from __future__ import annotations

from base64 import b64decode
from typing import Optional, Union

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PublicKey


HashableKey = Union[
    rsa.RSAPublicKey,
    EllipticCurvePublicKey,
    Ed25519PublicKey,
    Ed448PublicKey,
]


def _load_public_key(pem: Union[str, bytes]) -> HashableKey:
    if isinstance(pem, str):
        pem = pem.encode('utf-8')
    return serialization.load_pem_public_key(pem)  # type: ignore[return-value]


def _hash_for(name: str):
    name = name.upper()
    mapping = {
        'SHA256': hashes.SHA256,
        'SHA384': hashes.SHA384,
        'SHA512': hashes.SHA512,
    }
    if name not in mapping:
        raise ValueError(f'Unsupported hash algorithm: {name}')
    return mapping[name]()


def verify_signature(
    public_key: Union[HashableKey, str, bytes],
    data: bytes,
    signature: Union[bytes, str],
    *,
    algorithm: str = 'SHA256',
    strict: bool = True,
    allow_legacy: bool = False,
) -> bool:
    """
    Vérifie une signature sur `data`.

    - `public_key` : objet clé publique OU PEM (str/bytes)
    - `signature`  : bytes ou base64 (str)
    - `algorithm`  : SHA256 (défaut), SHA384, SHA512
    - `allow_legacy` : autorise RSA PKCS1v15 + SHA1 si True (déconseillé)
    """
    if isinstance(public_key, (str, bytes)):
        public_key = _load_public_key(public_key)

    if isinstance(signature, str):
        # on accepte une signature encodée base64
        try:
            signature = b64decode(signature, validate=True)
        except Exception:
            # ce n'est pas du base64 valide, on tente brut (rare)
            signature = signature.encode('utf-8')

    try:
        # Ed25519 / Ed448 ont une API dédiée (pas de hash/padding)
        if isinstance(public_key, (Ed25519PublicKey, Ed448PublicKey)):
            public_key.verify(signature, data)  # type: ignore[arg-type]
            return True

        # EC et RSA classiques
        if isinstance(public_key, rsa.RSAPublicKey):
            if algorithm.upper() == 'SHA1' and not allow_legacy:
                if strict:
                    return False
                # sinon on continue (legacy toléré sans échouer dur)
            hash_alg = hashes.SHA1() if algorithm.upper() == 'SHA1' else _hash_for(
                algorithm
            )
            public_key.verify(  # type: ignore[arg-type]
                signature,
                data,
                padding.PKCS1v15(),
                hash_alg,
            )
            return True

        # ECDSA
        if isinstance(public_key, EllipticCurvePublicKey):
            hash_alg = _hash_for(algorithm)
            from cryptography.hazmat.primitives.asymmetric import ec

            public_key.verify(  # type: ignore[arg-type]
                signature,
                data,
                ec.ECDSA(hash_alg),
            )
            return True

        # Clé non reconnue
        return False
    except Exception:
        return False
