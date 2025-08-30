# MEVE — Verification Guide (User)

A `*.meve.json` file certifies:
- the **existence** of a document at a given UTC timestamp,
- the **integrity** of its content (SHA-256 hash of bytes),
- the **issuer link** (Personal / Pro / Official, *computed by the verifier*).

> ⚠️ MEVE certifies the **bytes** of a file, not the “truth” of its content.

---

## 1) Verifying a `.meve.json` (web interface – upcoming)
- Open **DigitalMeve → Verify**.
- Drag & drop the file `myfile.ext.meve.json`.
- The verifier will show:
  - **Status**: Valid / Invalid
  - **Reason** in case of failure (e.g. *Missing required keys*, *hash mismatch*, *issuer mismatch*)
  - **Details**: filename, size, hash, timestamp, certification level (Personal/Pro/Official)

---

## 2) Verifying in Python (library)

```python
from digitalmeve.core import verify_meve

ok, info = verify_meve("myfile.pdf.meve.json", expected_issuer=None)
if ok:
    print("✔ Valid:", info["subject"]["filename"], info["subject"]["hash_sha256"])
else:
    print("✘ Invalid:", info.get("error"))
expected_issuer (optional): enforce the expected issuer (e.g. "DigitalMeve Test Suite").

Return value:

(True, info_dict) if valid,

(False, {"error": "...", ...}) if invalid.




---

3) Standard error messages

Missing required keys
→ Some mandatory keys are missing at the root or in subject.
Example:

{ "error": "Missing required keys", "missing": ["metadata", "timestamp"] }

hash mismatch
→ hash ≠ subject.hash_sha256 (internal inconsistency).

issuer mismatch
→ expected_issuer does not match the file issuer.

invalid file: …
→ The file is not valid JSON, corrupted, or not found.



---

4) What to do if invalid?

Re-generate the proof from the original document.

Ensure the file was not modified after generation.

Check the expected issuer if you enforce one (Pro/Official).



---

5) Best practices

Always keep the .meve.json next to the original file (same folder).

When sending, include both (zip or two attachments).

For large files (>50 MB), always use the sidecar file (*.meve.json).

Timestamps are UTC only (local time may differ).



---

6) Legal disclaimer

MEVE proves who froze which bytes at which moment.

It is not a civil identity unless Pro/Official flows are used.

Legal value depends on jurisdiction; MEVE aims at technical interoperability and traceability.



---

📚 More examples: docs/examples.md
📖 Full specification: docs/specification.md
