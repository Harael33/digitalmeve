# Contribuer à DigitalMeve

Merci de votre intérêt ! Pour contribuer :

## Flux de contribution
1. Ouvrez une **issue** si vous proposez une nouvelle fonctionnalité ou signalez un bug.
2. **Forkez** le dépôt puis créez une branche : `git checkout -b feature/ma-feature`
3. Écrivez du code **clair** + **tests** dans `tests/`.
4. Vérifiez que la **CI est verte** (lint, format, tests).
5. Ouvrez une **Pull Request** vers `main` (remplissez le template).

## Standards
- Python **3.10+**
- **pytest** pour les tests (`pytest -q`)
- **ruff** (lint) : `ruff check .`
- **black** (format) : `black .` (ligne 100 max)

## Commit & PR
- Messages de commit clairs : `feat: …`, `fix: …`, `docs: …`, `chore: …`
- Une PR = un sujet. Ajoutez captures/logs si pertinent.

## Sécurité
- Ne joignez **jamais** de documents sensibles aux issues/PR.
- Pour signaler une vulnérabilité : voir `SECURITY.md`.

Merci ! 🙏
