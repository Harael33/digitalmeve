"""
Core functions for DigitalMeve (.meve format)
"""

from pathlib import Path
import hashlib
import time


def generate_meve(file_path: str) -> dict:
    """
    Generate a MEVE certification (hash + timestamp) for a given file.
    """
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file, "rb") as f:
        content = f.read()
    digest = hashlib.sha256(content).hexdigest()

    return {
        "file": file.name,
        "timestamp": int(time.time()),
        "hash": digest,
    }


def verify_meve(file_path: str, expected_hash: str) -> bool:
    """
    Verify a file against a given SHA-256 hash.
    """
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file, "rb") as f:
        content = f.read()
    digest = hashlib.sha256(content).hexdigest()

    return digest == expected_hash
