import argparse
from src.digitalmeve.core import generate_meve


def main() -> None:
    parser = argparse.ArgumentParser(description="Générer un fichier .meve (preuve d'existence et d'intégrité).")
    parser.add_argument("--in", dest="infile", required=True, help="Fichier d'entrée (ex: facture.pdf)")
    parser.add_argument("--out", dest="outfile", required=True, help="Fichier .meve de sortie (ex: facture.meve)")
    parser.add_argument("--issuer", required=True, help="Émetteur (ex: Mon Entreprise)")
    args = parser.parse_args()

    out = generate_meve(args.infile, args.outfile, args.issuer)
    print(f"✅ Fichier .meve généré : {out}")


if __name__ == "__main__":
    main()
