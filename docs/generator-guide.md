# MEVE — Generator Guide (Developer)

This guide explains how to generate `.meve.json` proof files with **DigitalMeve**.

---

## 1) Quick start (Python)

```python
from digitalmeve.core import generate_meve

meve = generate_meve("myfile.pdf", issuer="My Company")
print(meve)

Result (dict example):

{
  "meve_version": "1.0",
  "issuer": "My Company",
  "timestamp": "2025-08-30T12:00:00Z",
  "metadata": {},
  "subject": {
    "filename": "myfile.pdf",
    "size": 12345,
    "hash_sha256": "abcdef123456...",
  },
  "hash": "abcdef123456...",
  "preview_b64": "..."
}


---

2) Output file (sidecar)

By default, generate_meve only returns a Python dict.

To save as file:


meve = generate_meve("myfile.pdf", outdir="out", issuer="My Company")

This creates:

out/myfile.pdf.meve.json


---

3) Fields explanation

meve_version → current version ("1.0")

issuer → issuer name (Personal, Pro, or Official)

timestamp → UTC ISO8601

metadata → free key-value (optional)

subject → description of the certified file

filename → original filename

size → file size in bytes

hash_sha256 → SHA-256 hash of file content


hash → same as subject.hash_sha256 (top-level shortcut)

preview_b64 → short base64 preview (first bytes of file)



---

4) Error handling

File not found → FileNotFoundError

Permission denied → standard Python OSError

Unsupported input type → TypeError if not str or Path



---

5) Best practices

Always generate the .meve.json immediately after finalizing a document.

Store .meve.json in the same folder as the file.

For Pro/Official issuers, use verified identity flow (coming soon).

Never modify .meve.json manually — any edit invalidates the proof.



---

📚 Next: Verification Guide
📖 Full specification: Specification

---
