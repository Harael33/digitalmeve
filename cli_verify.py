#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from digitalmeve import verify_meve


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Vérifie une preuve MEVE (fichier *.meve.json)."
    )
    parser.add_argument(
        "meve",
        help="Chemin vers le fichier *.meve.json à vérifier",
    )
    parser.add_argument(
        "--issuer",
        default=None,
        help="Issuer attendu (optionnel).",
    )
    args = parser.parse_args()

    ok, info = verify_meve(Path(args.meve), expected_issuer=args.issuer)
    if ok:
        print("MEVE valid ✓")
        return 0

    print("MEVE invalid ✗")
    print(info)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
