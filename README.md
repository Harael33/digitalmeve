# DigitalMeve — The Certified Digital Memory (.MEVE)

[![Tests](https://github.com/BACOUL/digitalmeve/actions/workflows/tests.yml/badge.svg)](https://github.com/BACOUL/digitalmeve/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Vision (v8)
DigitalMeve crée un **format universel de preuve numérique** : le **.MEVE (Memory Verified)** — un fichier texte minimal, **lisible en 2 secondes**, qui prouve :
1) **L’existence** d’un document à une date donnée  
2) **L’intégrité** du document (hash SHA-256)  
3) **L’authenticité de l’émetteur** (particulier, pro, institution)

Objectif : devenir le **“PDF de la preuve numérique”**.

---

## 🔑 Niveaux de certification
- **Personal** → auto-certification (preuve d’existence)  
- **Pro** → email vérifié (liée à une identité réelle)  
- **Official** → domaine DNS / institution vérifiée (preuve officielle)

> Le **statut est calculé par le vérificateur**, jamais déclaré manuellement → pas de triche.

---

## 📂 Spécification du format (MEVE/1)
Exemple de contenu (voir `docs/SPEC_MEVE_v1.md` pour le détail) :

MEVE/1 Status: Official | Pro | Personal Issuer: <identité> Certified: DigitalMeve (dns|email|self) Time: <horodatage UTC ISO 8601> Hash-SHA256: <empreinte> ID: <code court> Signature: <base64 Ed25519>   # optionnel pour MVP Meta: <nom fichier> • <taille bytes> • <mime> Doc-Ref: <référence interne optionnelle>

---

## 🧪 Démonstrations & exemples
- Dossier **`examples/`** :
  - `invoice.meve.json` (facture)
  - `diploma.meve.json` (diplôme)
- Vérificateur (MVP) : _drag & drop_ d’un `.meve` **+** du fichier original → **OK / KO** immédiat (hash).

---

## 🛠️ MVP (Phase 1 – 1 à 2 mois)
- Générateur `.meve` (site + script)
- Vérificateur `.meve` (site)
- SHA-256 + horodatage + ID (et **signature Ed25519** dans v1.1)

Roadmap détaillée : `docs/SPEC_MEVE_v1.md`.

---

## 💼 Modèle économique
- **Gratuit** : particuliers (preuve perso)
- **Abonnement/API** : entreprises (factures, contrats)
- **Licence officielle** : institutions (universités, administrations)

---

## 🔒 Sécurité & limites (MVP)
- Le `.meve` prouve **l’existence et l’intégrité du contenu** à une date T.  
- Il **ne garantit pas** la véracité d’un **faux document** émis par un particulier.  
- Pour les **preuves “officielles”**, l’émetteur doit être **vérifié** (DNS, email de domaine, clé officielle).  
- Détails et disclaimers : `docs/FAQ.md`.

---

## 🧩 Pour les développeurs
Installation locale (pour contribuer) :
```bash
pip install -e .
pytest -q

Points d’entrée Python (MVP) :

from digitalmeve import __version__
# Le code Python est le moteur technique pour générer/valider les .meve (MVP)


---

🤝 Contribuer

Problèmes → Issues (bug/feature)

PR bienvenues (voir CONTRIBUTING.md)

Templates d’issues → .github/ISSUE_TEMPLATE/



---

📜 Licence

MIT — voir LICENSE.

---

# 2) `docs/SPEC_MEVE_v1.md`

Crée ce fichier et colle :

```markdown
# Spécification MEVE/1 (MVP)

## 1. Objet
Le `.meve` est un **fichier JSON** minimal renseignant une **preuve d’existence, d’intégrité et d’émetteur** pour un document donné.

## 2. Champs obligatoires
- `format`: `"MEVE"`
- `version`: `"1"`
- `doc.name`: nom du fichier d’origine
- `doc.mime`: type MIME
- `doc.size`: taille en octets
- `doc.sha256`: empreinte SHA-256 hex du fichier original
- `generated_at`: horodatage UTC ISO 8601 (sans microsecondes)
- `issuer`: identité telle que déclarée (string normalisée)
- `id`: identifiant court (recommandé)
- `signature`: **optionnelle** en v1 (prévue v1.1 Ed25519 base64)

## 3. Exemple
```json
{
  "format": "MEVE",
  "version": "1",
  "doc": {
    "name": "invoice_2025_0001.pdf",
    "mime": "application/pdf",
    "size": 123456,
    "sha256": "ab12…ef34"
  },
  "issuer": "acme-ltd@example.com",
  "generated_at": "2025-08-27T10:15:00Z",
  "id": "K7R9-2M",
  "signature": ""
}

4. Niveaux (calculés côté vérif.)

Personal : issuer (email libre)

Pro : issuer validé par email

Official : issuer validé par DNS (_dm-meve TXT) ou clé officielle


5. Vérification

Recalcul SHA-256 du fichier fourni → égal à doc.sha256 ?

Si issuer vérifié (DNS/email), afficher badge correspondant.

Affichage clair : OK (intègre) / KO (altéré) / Unknown (source non-vérifiée).


6. Limites (MVP)

Preuve liée au contenu binaire, pas à la présentation (un PDF optimisé peut changer de hash).

Pour documents volumineux (>50 Mo), fallback autorisé : .meve.json séparé.

Formats sans métadonnées → sidecar .meve.json.


7. Évolutions (v1.1+)

Signature Ed25519 (base64)

Export PDF avec pied-de-page “Certifié par DigitalMeve”

API pro + intégrations ERP/Universités


---

# 3) `docs/FAQ.md`

```markdown
# FAQ — DigitalMeve

## DigitalMeve certifie-t-il l’authenticité d’un faux document ?
Non. Le `.meve` prouve **existence + intégrité** d’un contenu à une date T.  
L’**authenticité de la source** est garantie **uniquement** pour les statuts **Pro/Official** (email/DNS/clé).

## Et si je perds mon `.meve` ?
Vous pouvez **régénérer** une preuve si vous possédez encore le fichier original (le hash restera identique).  
Sinon, la preuve est perdue.

## Pourquoi le hash change parfois sur des PDF “optimisés” ?
Parce que la **représentation binaire** a changé. Le contenu visuel peut sembler identique, mais le hash est calculé sur les **octets**, pas sur l’apparence.

## Les institutions ?
Elles obtiennent un **badge Official** via un enregistrement **DNS** ou une **clé** fournie (future API).

## Aspects légaux
DigitalMeve ne remplace ni notaire ni horodatage qualifié eIDAS.  
Il fournit une **preuve technique** d’existence/intégrité/émission, utilisable comme **indice**.


---

4) examples/README.md + exemples

examples/README.md :

# Exemples .MEVE

- `invoice.meve.json` : facture exemple
- `diploma.meve.json` : diplôme exemple

Chaque fichier `.meve.json` est un **exemple** de payload MEVE/1 tel que spécifié dans `docs/SPEC_MEVE_v1.md`.

examples/invoice.meve.json :

{
  "format": "MEVE",
  "version": "1",
  "doc": {
    "name": "invoice_2025_0001.pdf",
    "mime": "application/pdf",
    "size": 123456,
    "sha256": "ab12cd34ef..."
  },
  "issuer": "billing@acme.example",
  "generated_at": "2025-08-27T10:15:00Z",
  "id": "INV-K7R9-2M",
  "signature": ""
}

examples/diploma.meve.json :

{
  "format": "MEVE",
  "version": "1",
  "doc": {
    "name": "diploma_alice.pdf",
    "mime": "application/pdf",
    "size": 234567,
    "sha256": "98ab76cd54..."
  },
  "issuer": "registrar@university.example",
  "generated_at": "2025-08-27T10:20:00Z",
  "id": "UNI-9P3X-1Q",
  "signature": ""
}


---

5) Templates GitHub (issues / PR)

Créer .github/ISSUE_TEMPLATE/bug_report.md :

---
name: Bug report
about: Signaler un bug
labels: bug
---

**Description**
Que s’est-il passé ?

**Étapes pour reproduire**
1. …
2. …

**Comportement attendu**
…

**Captures / logs**
…

Créer .github/ISSUE_TEMPLATE/feature_request.md :

---
name: Feature request
about: Proposer une amélioration
labels: enhancement
---

**Problème / besoin**
…

**Solution proposée**
…

**Alternatives**
…

**Contexte**
…

Créer .github/PULL_REQUEST_TEMPLATE.md :

## Objet
(quoi / pourquoi)

## Changements
- …

## Checklist
- [ ] Tests OK
- [ ] Docs/README mis à jour si nécessaire

