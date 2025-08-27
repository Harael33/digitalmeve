#!/usr/bin/env python3
import argparse, sys
from src.generator import generate_meve

def main():
    p = argparse.ArgumentParser(description="DigitalMeve — Générer un .meve pour un document")
    p.add_argument("document", help="Chemin du document source (ex: facture.pdf)")
    p.add_argument("--issuer", help="Identité de l’émetteur (email/nom)", default=None)
    p.add_argument("--out", help="Chemin de sortie du .meve.json", default=None)
    args = p.parse_args()

    try:
        out = generate_meve(args.document, issuer=args.issuer, output_path=args.out)
        print(f"✅ Preuve MEVE générée : {out}")
    except Exception as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
