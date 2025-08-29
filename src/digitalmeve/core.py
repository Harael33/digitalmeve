"""
Core functions for DigitalMeve (.meve format)
Simple reference implementation for MVP.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass
class Meve:
    version: str
    issuer: str
    issued_at: str  # ISO8601
    target_filename: str
    target_size: int
    target_hash_algo: str
    target_hash_value: str


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def generate_meve(infile: str, outfile: str, issuer: str) -> Path:
    """
    Generate a .meve sidecar file (JSON) for the given input file.
    - Computes SHA-256 over the raw file bytes
    - Stores minimal, human-readable proof

    Returns: Path to the created .meve file
    """
    src = Path(infile)
    if not src.exists() or not src.is_file():
        raise FileNotFoundError(f"Input file not found: {infile}")

    # Read content & hash
    data = src.read_bytes()
    digest = _sha256_hex(data)

    # Minimal ISO time without importing extra deps
    # (safe enough for MVP; we can swap to RFC3339 precisely later)
    from datetime import datetime, timezone

    issued_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload = {
        "version": "1.0",
        "issuer": issuer,
        "issued_at": issued_at,
        "target": {
            "filename": src.name,
            "size": len(data),
            "hash": {"algo": "SHA-256", "value": digest},
        },
        "signature": None,  # reserved (v1.7+)
    }

    out = Path(outfile)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def verify_meve(meve_file: str, expected_issuer: str) -> Tuple[bool, str]:
    """
    Verify a .meve file against its referenced target file:
    - checks issuer
    - recomputes SHA-256 from target file bytes
    - compares with recorded hash

    Returns: (ok, details)
    """
    p = Path(meve_file)
    if not p.exists() or not p.is_file():
        return False, f"MEVE file not found: {meve_file}"

    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"Invalid MEVE JSON: {e!r}"

    # Basic schema checks
    try:
        issuer = obj["issuer"]
        issued_at = obj["issued_at"]
        target = obj["target"]
        filename = target["filename"]
        algo = target["hash"]["algo"]
        expected_hash = target["hash"]["value"]
    except KeyError as e:
        return False, f"Missing required field: {e!r}"

    if issuer != expected_issuer:
        return False, f"Issuer mismatch: expected '{expected_issuer}' got '{issuer}'"

    if algo.upper() != "SHA-256":
        return False, f"Unsupported hash algo: {algo}"

    # Locate target file in the same folder as the .meve (common case)
    target_path = p.parent / filename
    if not target_path.exists() or not target_path.is_file():
        return False, f"Target file not found next to MEVE: {target_path.name}"

    # Recompute hash
    digest = _sha256_hex(target_path.read_bytes())

    if digest != expected_hash:
        return False, "Hash mismatch: file content differs from recorded proof"

    # Passed all checks
    return True, f"Valid MEVE for '{filename}' at {issued_at}"
