# DigitalMeve — Pro Verification (Spec Draft)

## Goal
Link a `.MEVE` proof to a **real professional identity** (company or freelancer) via a verified business email and (later) domain checks.

## Status Levels
- `Personal` → self-asserted (free)
- **`Pro` → verified email** at a business domain (paid)
- `Official` → verified DNS + org key (future / see OFFICIAL.md)

## Minimal Pro Flow (MVP+1)
1) User signs in with email `name@company.tld` (magic link / one-time code).
2) We generate `.MEVE` with:
   - `Status: Pro`
   - `Issuer: email`
   - `Certified: DigitalMeve (email)`
   - `Time, Hash-SHA256, ID`
   - `Signature: Ed25519 (base64)`
3) Verifier checks signature + hash and confirms `Pro (email verified)`.

## Email Verification
- Transport: one-time link or 6-digit code (10 min TTL).
- Policy: deny disposable domains; allow public ISPs but **mark as Pro only if domain looks professional** (configurable).

## UX copy (short)
- “Pro means: email verified at a real domain. It links the proof to a professional identity, not to a person’s legal identity.”

## Future
- Link email → DNS (`@acme.com` → `acme.com` TXT record) to auto-upgrade to `Official` once DNS is verified.
