#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DigitalMeve — CLI verifier
Command:  meve-verify
But:      Vérifier un fichier .meve (ou .meve.json) par rapport à un document
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List

# Le code du projet est dans le package "src"
from src.verifier import verify_meve  # doit exister


def guess_meve_path(document_path: str) -> str | None:
    """
    Devine le chemin du .meve à partir du document :
      - <doc>.meve
      - <doc>.meve.json
    """
    candidates = [document_path + ".meve", document_path + ".meve.json"]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="meve-verify",
        description="Verify a .meve proof file against a document"
    )
    parser.add_argument(
        "document",
        help="Path to the original document (ex: invoice.pdf)"
    )
    parser.add_argument(
        "--meve",
        help="Path to the .meve or .meve.json file (default: try <document>.meve or .meve.json)"
    )

    args = parser.parse_args(argv)

    doc_path = args.document
    if not os.path.isfile(doc_path):
        print(f"[ERROR] Document not found: {doc_path}", file=sys.stderr)
        return 1

    meve_path = args.meve or guess_meve_path(doc_path)
    if not meve_path:
        print(
            "[ERROR] Could not locate the proof file. "
            "Use --meve <path.meve|path.meve.json> or place it next to the document.",
            file=sys.stderr,
        )
        return 1

    try:
        with open(meve_path, "r", encoding="utf-8") as f:
            meve_text = f.read()
    except Exception as exc:
        print(f"[ERROR] Cannot read proof file '{meve_path}': {exc}", file=sys.stderr)
        return 1

    try:
        ok, details = verify_meve(document_path=doc_path, meve_text=meve_text)
    except TypeError:
        # Compat pour ancienne signature potentielle
        ok = verify_meve(doc_path, meve_text)  # type: ignore[call-arg]
        details = None
    except Exception as exc:
        print(f"[ERROR] Verification failed: {exc}", file=sys.stderr)
        return 1

    if ok:
        print("✅ Verified — document matches its .MEVE proof")
        print(f" • Document : {doc_path}")
        print(f" • Proof    : {meve_path}")
        if details:
            print(f" • Details  : {details}")
        return 0
    else:
        print("❌ Verification failed — content mismatch or invalid proof", file=sys.stderr)
        print(f" • Document : {doc_path}", file=sys.stderr)
        print(f" • Proof    : {meve_path}", file=sys.stderr)
        if details:
            print(f" • Details  : {details}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
