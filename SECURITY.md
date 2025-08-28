# Security Policy

## Supported Versions
Nous maintenons uniquement les dernières versions mineures stables de DigitalMeve.  
| Version | Supportée |
|---------|-----------|
| 0.1.x   | ✅ |
| < 0.1   | ❌ |

---

## Signalement de vulnérabilités
Si vous découvrez une faille de sécurité :
1. **Ne pas ouvrir d’issue publique.**
2. Envoyer un mail à : `security@digitalmeve.org`
3. Indiquer :
   - Version concernée
   - Étapes de reproduction
   - Impact potentiel

Nous nous engageons à répondre **sous 48 heures** et à proposer un correctif **sous 7 jours ouvrés**.

---

## Process de correction
- Patch appliqué sur `main` via PR privée
- Release patch (`vX.Y.Z+security`)
- Publication dans `CHANGELOG.md`
- Notification aux utilisateurs via PyPI + GitHub Release

---

## Bonnes pratiques pour les développeurs
- Toujours valider la **signature cryptographique** avant d’accepter un fichier `.meve`
- Ne pas stocker les clés privées dans le repo
- Utiliser uniquement les dépendances listées dans `requirements.txt`
- Vérifier l’intégrité avec `cli_verify.py` avant utilisation

---

## Certifications prévues
DigitalMeve vise les niveaux suivants :
- ✅ **SHA-256 Hashing** — déjà implémenté
- ✅ **Ed25519 Signatures** — déjà implémenté
- 🔜 **ISO 27001 compliant workflows**
- 🔜 **EU eIDAS compatible trust services**
