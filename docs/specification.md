# DigitalMeve — MEVE/1 Specification (draft)

## 1) Purpose
`.meve` provides a portable, human-readable proof for any digital file:
- Existence at time T (UTC timestamp)
- Integrity of the exact bytes (SHA-256)
- Issuer linkage (Personal / Pro / Official), **computed by the verifier** — never user-declared

## 2) Minimal JSON (MEVE/1)

```json
{
  "issuer": "Personal",
  "meve_version": "1.0",
  "hash": "<sha256 of the file>",
  "preview_b64": "<optional base64 preview of first bytes>",
  "subject": {
    "filename": "sample.pdf",
    "size": 12345,
    "hash_sha256": "<sha256 of the file>"
  },
  "timestamp": "2025-08-30T12:34:56Z",
  "metadata": {}
}
