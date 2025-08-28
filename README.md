# digitalmeve

[![Tests](https://github.com/BACOUL/digitalmeve/actions/workflows/tests.yml/badge.svg)](https://github.com/BACOUL/digitalmeve/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/digitalmeve.svg)](https://pypi.org/project/digitalmeve/)
[![Python versions](https://img.shields.io/pypi/pyversions/digitalmeve.svg)](https://pypi.org/project/digitalmeve/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Downloads](https://static.pepy.tech/badge/digitalmeve)](https://pepy.tech/project/digitalmeve)

---

## 📖 Description

**digitalmeve** est une librairie Python simple et légère pour :

- Générer des identités ou jetons uniques (`generate_meve`)  
- Vérifier des identités ou données (`verify_identity`)  
- Manipuler et formater des identités (`format_identity`)  

Elle est pensée pour être **rapide, fiable et facilement intégrable** dans vos projets Python.

---

## 📦 Installation

Depuis **PyPI** :

```bash
pip install digitalmeve


---

🚀 Exemple d’utilisation

from digitalmeve import generate_meve, verify_identity, format_identity, __version__

# Génération d’un identifiant
meve_id = generate_meve("Alice", issuer="digitalmeve")
print(meve_id)

# Vérification d’identité
data = {"name": "Alice", "issuer": "digitalmeve"}
print(verify_identity(data, expected_issuer="digitalmeve"))  # True

# Formatage d’identité
print(format_identity({"name": "Alice", "age": 30}))


---

✅ Tests

Pour exécuter les tests unitaires :

pytest

Les tests sont automatiquement lancés via GitHub Actions sur chaque commit/pull request.


---

🤝 Contribution

1. Forkez le repo


2. Créez une branche (git checkout -b feature/ma-feature)


3. Faites vos changements


4. Poussez (git push origin feature/ma-feature)


5. Ouvrez une Pull Request 🎉




---

📌 Roadmap

[x] Génération d’identifiants uniques

[x] Vérification d’identité

[x] Tests automatisés (CI/CD)

[ ] Ajout de signatures cryptographiques

[ ] Support multi-issuer

[ ] Documentation hébergée (ReadTheDocs / MkDocs)



---

📄 License

Ce projet est sous licence MIT – vous êtes libre de l’utiliser et de le modifier.
Voir le fichier LICENSE pour plus de détails.
