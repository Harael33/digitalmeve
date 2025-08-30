# Examples of MEVE usage

## Example 1 — Basic file proof
Input file: `contract.pdf`

Generated proof (`contract.pdf.meve.json`):
```json
{
  "meve_version": "1.0",
  "issuer": "Personal",
  "timestamp": "2025-08-30T12:00:00Z",
  "subject": {
    "filename": "contract.pdf",
    "size": 52344,
    "hash_sha256": "abcd1234..."
  },
  "hash": "abcd1234...",
  "metadata": {}
}

Verification:

digitalmeve verify contract.pdf.meve.json
✔ Valid — hash and issuer verified


---

Example 2 — With metadata

Input file: photo.jpg

Proof snippet:

{
  "subject": {
    "filename": "photo.jpg",
    "size": 238900,
    "hash_sha256": "efgh5678..."
  },
  "metadata": {
    "location": "Paris",
    "author": "Alice"
  }
}


---

Example 3 — Professional certification

Issuer: DigitalMeve Pro Test Suite

Proof includes:

Verified email → issuer level = Pro

Standard JSON with extra field "issuer_level": "Pro"

