# DigitalMeve — The Certified Digital Memory

[![Tests](https://github.com/<votre-user>/<votre-repo>/actions/workflows/python-app.yml/badge.svg)](https://github.com/<votre-user>/<votre-repo>/actions)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

---

## 🚀 Vision

**DigitalMeve** crée un nouveau format universel de certification numérique : le **.MEVE (Memory Verified)**.  
Un format simple, lisible en 2 secondes, qui prouve :

- 📌 L’existence d’un document à une date donnée  
- 🔒 L’intégrité du document (empreinte SHA-256)  
- ✅ L’authenticité de l’émetteur (particulier, professionnel ou institution)  

👉 Objectif : devenir le **“PDF de la preuve numérique”** à l’international.  

---

## 📂 Exemple de fichier `.meve`

```txt
MEVE/1
Status: Pro
Issuer: contact@exemple.com
Certified: DigitalMeve (email verified)
Time: 2025-08-27T22:35:01Z
Hash-SHA256: 5f2a6c4f6b7d2f9c3f8a8d...
ID: MEVE-9XJ3L
Signature: 6Jf8aA9sd8as7d8as9== (base64 Ed25519)
Meta: facture.pdf • 18230 bytes • application/pdf
Doc-Ref: facultatif

Lisible immédiatement → pas besoin d’outils complexes.


---

📦 Installation

Clonez le dépôt et installez les dépendances :

git clone https://github.com/<votre-user>/<votre-repo>.git
cd <votre-repo>
pip install -r requirements.txt


---

🛠️ Utilisation

Générer un fichier .meve

python -m utils.generate path/to/document.pdf

Résultat → document.pdf.meve

Vérifier un fichier .meve

python -m utils.verify path/to/document.pdf.meve

Résultat → ✔ Document vérifié ou ❌ Document invalide


---

✅ Tests

Exécuter la suite de tests :

pytest tests/


---

🤝 Contribution

Les contributions sont les bienvenues !

Forkez le dépôt

Créez une branche (git checkout -b feature-nouvelle)

Committez vos changements (git commit -m "Ajout d'une nouvelle feature")

Poussez (git push origin feature-nouvelle)

Ouvrez une Pull Request



---

📜 Licence

Ce projet est sous licence MIT — voir le fichier LICENSE.


---

🌍 Liens utiles

Site officiel : https://digitalmeve.com (placeholder)

Documentation technique : bientôt disponible

Contact : support@digitalmeve.com
