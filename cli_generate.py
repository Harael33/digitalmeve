#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DigitalMeve — CLI generator
Command:  meve-generate
But:      Générer un fichier .meve (ou .meve.json en fallback) pour un document
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Dict, Any, List

# Le code du projet est dans le package "src"
from src.generator import generate_meve  # doit exister


def parse_meta(pairs: List[str]) -> Dict[str, Any]:
    """
    Convertit des 'key=value' en dict. Ex: --meta ref=FAC-2025 client=ACME
    """
    meta: Dict[str, Any] = {}
    for p in pairs or []:
        if "=" not in p:
            raise argparse.ArgumentTypeError(
                f"Invalid --meta item '{p}'. Use key=value."
            )
        k, v = p.split("=", 1)
        k = k.strip()
        v = v.strip()
        if not k:
            raise argparse.ArgumentTypeError("Empty key in --meta")
        # Tente de parser JSON simple (true/false/num/list/obj)
        try:
            meta[k] = json.loads(v)
        except Exception:
            meta[k] = v
    return meta


def default_meve_path(document_path: str, sidecar: bool) -> str:
    base = document_path + ".meve"
    return base + ".json" if sidecar else base


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="meve-generate",
        description="Generate a .meve proof file for a document"
    )
    parser.add_argument(
        "document",
        help="Path to the source document (ex: invoice.pdf)"
    )
    parser.add_argument(
        "--issuer-email",
        dest="issuer_email",
        required=True,
        help="Issuer email to embed in the proof (ex: contact@example.com)",
    )
    parser.add_argument(
        "--status",
        default="Pro",
        help="Optional status field (default: Pro)"
    )
    parser.add_argument(
        "--meta",
        nargs="*",
        metavar="key=value",
        help="Optional metadata pairs (ex: ref=FAC-2025 client=ACME amount=123.45)"
    )
    parser.add_argument(
        "--output",
        help="Where to write the .meve file (default: <document>.meve or .meve.json)",
    )
    parser.add_argument(
        "--force-sidecar",
        action="store_true",
        help="Force sidecar JSON (.meve.json) instead of inline .meve",
    )

    args = parser.parse_args(argv)

    doc_path = args.document
    if not os.path.isfile(doc_path):
        print(f"[ERROR] Document not found: {doc_path}", file=sys.stderr)
        return 1

    meta = parse_meta(args.meta)

    try:
        # La fonction du projet doit accepter issuer_email depuis nos derniers correctifs.
        meve_text = generate_meve(
            document_path=doc_path,
            issuer_email=args.issuer_email,
            status=args.status,
            meta=meta,
            save_sidecar_if_needed=args.force_sidecar,
        )
    except TypeError as te:
        # Aide si on a un vieux nom d’argument côté lib
        print(
            "[ERROR] generate_meve() signature mismatch. "
            "Assure-toi que la fonction accepte issuer_email=... "
            "et save_sidecar_if_needed=... ",
            file=sys.stderr,
        )
        print(str(te), file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[ERROR] Generation failed: {exc}", file=sys.stderr)
        return 1

    # Chemin de sortie final
    out_path = args.output or default_meve_path(
        doc_path, sidecar=args.force_sidecar
    )

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(meve_text)
    except Exception as exc:
        print(f"[ERROR] Cannot write output file '{out_path}': {exc}", file=sys.stderr)
        return 1

    print("✅ .MEVE proof generated")
    print(f" • Document : {doc_path}")
    print(f" • Output   : {out_path}")
    print(f" • Issuer   : {args.issuer_email}")
    if meta:
        print(f" • Meta     : {json.dumps(meta, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
