# Security Model (draft)

## What MEVE proves
- **Existence** at time T (UTC timestamp).
- **Integrity** of the exact bytes (SHA-256).
- **Issuer linkage** (Personal / Pro / Official) — level is computed by the verifier.

## What MEVE does NOT prove
- Civil/legal identity of a person by itself (unless verified flows are used).
- Truthfulness of the content; it certifies bytes, not meaning.

## Threats & mitigations
- **Tampering**: any byte change → different SHA-256 → verification fails.
- **Visual tricks**: verification relies on content hash, not on how a viewer renders it.
- **Large files** (>50 MB): prefer sidecar `*.meve.json` instead of metadata embedding.
- **Clock issues**: store timestamps in UTC ISO-8601; future option: trusted timestamp authority.
- **Key management (future)**: Pro/Official signatures will use per-issuer keys and revocation lists.

## Responsible disclosure
Please report vulnerabilities privately:
- Email: `security@digitalmeve.example`
- Expected first response: **≤ 72h**

Do not publicly disclose before a fix or mitigation is available.

## Scope
- Core library under `/src/digitalmeve`
- Reference verifier/generator
- CI workflows under `.github/workflows`

## Privacy
- No document content is stored by the verifier; only the hash and minimal metadata appear in proofs.
