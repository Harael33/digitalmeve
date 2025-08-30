# 🛡 DigitalMeve Verification Guide

## Overview
DigitalMeve provides a fast and universal way to verify the authenticity of any `.meve` proof.  
Verification ensures:
1. The document has not been tampered with (hash validation).  
2. The proof contains a valid timestamp (UTC).  
3. The issuer identity matches the expected level (Personal, Pro, Official).  

---

## Verification Methods

### 1. Local verification (Python SDK)
```bash
pip install digitalmeve

from digitalmeve import verify_meve

ok, info = verify_meve("sample.txt.meve.json", expected_issuer="DigitalMeve Test Suite")

if ok:
    print("✅ Proof valid:", info)
else:
    print("❌ Invalid proof:", info)


---

2. Web verification

Drag & drop your .meve.json file into the DigitalMeve Web Verifier (coming soon).

The verifier runs locally in your browser — no data is uploaded.



---

3. API verification

DigitalMeve will provide a REST API for professional integrations:

POST /api/v1/verify
Content-Type: application/json

{
  "proof": { ... }
}

Response:

{
  "valid": true,
  "issuer": "Pro",
  "timestamp": "2025-08-30T12:34:56Z",
  "hash": "b94d27b9934d3e08..."
}


---

Error Cases

issuer mismatch → Issuer does not match the expected identity.

hash mismatch → The document has been altered.

missing keys → Proof file is incomplete or corrupted.



---

Next Steps

See Generator Guide for creating proofs.

Check Security for technical guarantees.


---
