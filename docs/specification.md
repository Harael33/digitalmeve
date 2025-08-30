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
Required fields

issuer (string) – logical issuer name shown in proofs

meve_version (string) – currently "1.0"

hash (string) – SHA-256 of the exact file bytes; must equal subject.hash_sha256

preview_b64 (string) – short base64 preview; optional but present in our generator

subject (object)

filename (string) – original file name

size (integer) – size in bytes

hash_sha256 (string) – SHA-256 of the file


timestamp (string, ISO 8601 UTC)

metadata (object, can be empty)


3) Levels (computed by verifier)

Personal — self (default)

Pro — verified email/domain account (future)

Official — DNS / institution verified (future)


> The level is computed by the verifier’s rules and cannot be faked by setting a field.



4) Generation rules (reference)

Do not modify the original file; produce a sidecar *.meve.json.

Compute SHA-256 on the full byte stream.

Include a small preview_b64 (first ~64 bytes) to help quick visual checks.

Use datetime.now(timezone.utc).isoformat() for timestamp (UTC).


5) Verification rules (reference)

Given a dict or a path to *.meve.json, the verifier MUST:

1. Parse JSON → must be an object.


2. Check presence of required root keys:

issuer, meve_version, subject, hash, metadata, timestamp, preview_b64



3. Check subject contains filename, size, hash_sha256.


4. Check hash == subject.hash_sha256 (internal consistency).


5. If expected_issuer is provided, enforce equality.


6. Return (ok: true, info: dict) on success; otherwise (ok: false, {"error": "...", ...}).



Standard error messages

Missing root keys → {"error": "Missing required keys", "missing": [...] }

Issuer mismatch → {"error": "issuer mismatch", "expected": "..." }

Hash mismatch → {"error": "hash mismatch" }

Invalid JSON/file → {"error": "invalid file: <details>" }


6) Embedding vs. sidecar

Recommended (MVP): keep the original file untouched; emit a sidecar filename.ext.meve.json.

Future: metadata embedding (PDF/XMP, PNG tEXt, EXIF/XMP) when stable and standardized.


7) Backward/forward compatibility

Parsers must ignore unknown fields (extensibility).

meve_version guards major format changes (e.g., "2.0" in the future).


8) Security notes (short)

Any byte change → different SHA-256 → verification fails.

Existence proof ≠ legal identity. Identity-level comes from verified accounts (Pro/Official).

Timestamp is UTC; trusted timestamp authority may be added in a future revision.


9) Examples

See docs/examples.md for concrete invoice/photo/diploma samples.
