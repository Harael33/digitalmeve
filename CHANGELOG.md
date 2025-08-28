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

---

## Historique antérieur
- Prototypes et POC internes avant 0.1.5 (non publiés).

[Unreleased]: ../../compare/v0.1.5...HEAD
[0.1.5]: ../../releases/tag/v0.1.5
