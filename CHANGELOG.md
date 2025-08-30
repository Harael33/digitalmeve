# Changelog

All notable changes to this project will be documented in this file.
Format: Keep a Changelog. Versioning: Semantic Versioning.

## [Unreleased]

### Added
- Documentation scaffolding: specification, security, examples, roadmap.
- Issue templates (bug & feature), SECURITY, CONTRIBUTING, Code of Conduct.
- Dependabot & CODEOWNERS.

### Changed
- CI quality fixed (flake8 line length), consistent error messages.

### Fixed
- `generator.py`: adds `hash`, `preview_b64`, `timestamp`, `metadata`, `subject{}`.
- `verifier.py`: stable `(ok, info)` API; exact error wording (“Missing required keys”).
- `utils.py`: `format_identity()` handles `{"identity": ...}`.
- Tests aligned and passing on 3.10/3.11/3.12.

## [1.6.0] - 2025-08-30
Initial internal stabilization (no public release). All tests green, quality green.
## [1.6.0] - 2025-08-29
### Added
- Stabilisation publique de la branche **1.x** (passage en 1.6.0).
- Documentation initiale (overview/specification/examples).
- Module `core.py` (implémentation de base) + tests.

### Changed
- Alignement versionning (`__init__`, `pyproject.toml`, tests).
- Nettoyage et robustesse `pyproject.toml`.

### CI/CD
- Tests (Python 3.10–3.12) ✅
- Publication PyPI via **Trusted Publisher (OIDC)** prête.# Changelog — DigitalMeve

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
