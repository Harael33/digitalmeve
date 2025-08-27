#!/usr/bin/env python3
import argparse, sys
from src.verifier import verify_meve, read_meve_info

def main():
    p = argparse.ArgumentParser(description="DigitalMeve — Vérifier un document avec son .meve")
    p.add_argument("document", help="Chemin du document original")
    p.add_argument("meve", help="Chemin du fichier .meve.json")
    args = p.parse_args()

    try:
        ok = verify_meve(args.document, args.meve)
        info = read_meve_info(args.meve)
        if ok:
            print("✅ Vérification OK")
        else:
            print("❌ Vérification KO")
        print(f"ℹ️  Issuer: {info.get('Issuer')}")
        print(f"ℹ️  Time:   {info.get('Time')}")
        print(f"ℹ️  ID:     {info.get('ID')}")
    except Exception as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
