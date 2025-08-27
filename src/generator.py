import hashlib
import json
import base64
import time
import sys
from pathlib import Path

def generate_meve(file_path):
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError("File not found")

    # Lire le fichier
    content = file.read_bytes()

    # Hash SHA-256
    file_hash = hashlib.sha256(content).hexdigest()

    # Métadonnées MEVE
    meve_data = {
        "status": "Personal",  # Personal | Pro | Official
        "issuer": "anonymous",
        "certified": "DigitalMeve (self)",
        "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "hash_sha256": file_hash,
        "id": base64.urlsafe_b64encode(file_hash.encode()).decode()[:12],
        "meta": {
            "filename": file.name,
            "size": file.stat().st_size,
            "mime": "application/octet-stream"
        }
    }

    # Sauvegarde du fichier .meve
    output = file.with_suffix(file.suffix + ".meve")
    with open(output, "w", encoding="utf-8") as f:
        json.dump(meve_data, f, indent=2)

    print(f"✅ MEVE file generated: {output}")

# Exécution via CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generator.py <file>")
    else:
        generate_meve(sys.argv[1])
