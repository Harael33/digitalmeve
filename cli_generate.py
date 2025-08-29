#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from digitalmeve import generate_meve


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Génère un MEVE (*.meve.json) pour un fichier donné."
    )
    parser.add_argument(
        "infile",
        help="Chemin vers le fichier d'entrée",
    )
    parser.add_argument(
        "--outdir",
        default=None,
        help="Dossier de sortie (par défaut: dossier du fichier source)",
    )
    parser.add_argument(
        "--issuer",
        default="DigitalMeve CLI",
        help="Nom de l'émetteur inscrit dans la preuve",
    )
    args = parser.parse_args()

    outdir = Path(args.outdir) if args.outdir else None
    meve = generate_meve(args.infile, outdir=outdir, issuer=args.issuer)

    print("MEVE generated.")
    print(f"subject.filename: {meve['subject']['filename']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
