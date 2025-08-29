# Changelog — DigitalMeve

Ce projet suit [SemVer](https://semver.org/lang/fr/) et le format recommandé par [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## [Unreleased]
### Ajouté
- Pages de documentation initiales (`docs/overview.md`, `docs/specification.md`, `docs/examples.md`).
- Politique de sécurité complète (`SECURITY.md`).
- Guide de contribution (`CONTRIBUTING.md`).

### Modifié
- README : badges (tests, publish, PyPI, Python, downloads, licence) et liens vers la doc.

---

## [0.1.5] — 2025-08-28
### Ajouté
- Version initiale du format **.MEVE** (preuve d’existence & d’intégrité).
- Workflows GitHub Actions : `tests.yml` (CI) et `publish.yml` (PyPI Trusted Publisher).
- Configuration `pyproject.toml` et métadonnées Python (3.10–3.12).
- Première release publique (PyPI).

### Sécurité
- Hash **SHA-256** obligatoire.
- Base de signature **Ed25519** prévue (v1.1).
# Changelog
Toutes les modifications notables de ce projet seront documentées dans ce fichier.
Ce format suit [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/) et le versionnage [SemVer](https://semver.org/lang/fr/).

## [0.1.5] - 2025-08-29

### Added
- Nouveau module `digitalmeve.core` avec l’implémentation de référence du format **.MEVE** :
  - `generate_meve(data, issuer)` – génère un objet MEVE (horodatage + hash + signature simple).
  - `verify_meve(meve, expected_issuer)` – vérifie l’authenticité d’un MEVE.
- Export public mis à jour dans `digitalmeve/__init__.py` (import direct des fonctions cœur).

### Changed
- Métadonnées projet corrigées dans `pyproject.toml` (syntaxe TOML, découverte de packages, classifiers).

### Tests
- Nouveau `tests/test_core.py` couvrant génération & vérification (cas nominal).

### CI
- Workflow GitHub Actions **tests** au vert (Python 3.10–3.12).

### Notes
- Pas de breaking change ; les CLI existants continuent de fonctionner.

---

## [0.1.4] - 2025-08-XX
*(section antérieure si applicable — laissez telle quelle si elle existe déjà)*
---

## Historique antérieur
- Prototypes et POC internes avant 0.1.5 (non publiés).

[Unreleased]: ../../compare/v0.1.5...HEAD
[0.1.5]: ../../releases/tag/v0.1.5
