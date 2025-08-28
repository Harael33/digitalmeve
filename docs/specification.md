# 📜 DigitalMeve — Specification v0.1.5

Cette spécification décrit le format **.meve (Memory Verified)** tel qu’implémenté dans DigitalMeve v0.1.5.

---

## 1. Structure du fichier

Un fichier `.meve` est un objet JSON **lisible et universel**, avec les champs suivants :

```json
{
  "version": "0.1.5",
  "document_hash": "sha256:...",
  "timestamp": "2025-08-28T12:34:56Z",
  "issuer": "did:key:z6Mkh...",
  "signature": "ed25519:...",
  "metadata": {
    "name": "optional",
    "tags": ["optional"],
    "note": "optional"
  }
}
