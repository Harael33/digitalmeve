# src/utils.py
from __future__ import annotations
import hashlib, json, base64, time, os
from dataclasses import dataclass

ALGO = "SHA-256"

def sha256_file(path: str) -> str:
    """Retourne l'empreinte SHA-256 hex d'un fichier (streamé)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")

def utc_now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def file_meta(path: str) -> dict:
    st = os.stat(path)
    return {
        "name": os.path.basename(path),
        "size": st.st_size,
        "mime": "application/octet-stream",  # simplifié pour MVP
    }

@dataclass
class MeveDoc:
    status: str          # "Personal" | "Pro" | "Official"
    issuer: str          # email, domaine, ou "self"
    certified: str       # "DigitalMeve (email|dns|self)"
    time: str            # ISO UTC
    hash_hex: str        # SHA-256 hex du document source
    id: str              # identifiant court
    signature_b64: str   # signature Ed25519 en base64 (placeholder MVP)
    meta: dict           # name/size/mime
    doc_ref: str | None = None

    def to_text(self) -> str:
        obj = {
            "MEVE": "1",
            "Status": self.status,
            "Issuer": self.issuer,
            "Certified": self.certified,
            "Time": self.time,
            "Hash-SHA256": self.hash_hex,
            "ID": self.id,
            "Signature": self.signature_b64,
            "Meta": self.meta,
        }
        if self.doc_ref:
            obj["Doc-Ref"] = self.doc_ref
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
