import argparse
from src.digitalmeve.core import verify_meve


def main() -> None:
    parser = argparse.ArgumentParser(description="Vérifier un fichier .meve (intégrité + émetteur).")
    parser.add_argument("--file", required=True, help="Fichier .meve (ex: facture.meve)")
    parser.add_argument("--expected-issuer", required=True, help="Émetteur attendu (ex: Mon Entreprise)")
    args = parser.parse_args()

    ok, details = verify_meve(args.file, args.expected_issuer)
    if ok:
        print("✅ Vérification réussie —", details)
        raise SystemExit(0)
    else:
        print("❌ Vérification échouée —", details)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
