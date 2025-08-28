# 🌍 DigitalMeve — Overview

DigitalMeve est le **format universel (.meve)** pour *prouver, certifier et vérifier* l’authenticité d’un document numérique.

## Qu’est-ce qu’un fichier `.meve` ?
`.meve` = **Memory Verified** : un conteneur léger, lisible, qui regroupe :
- ✅ L’empreinte (hash) du document d’origine (SHA-256)
- ⏱️ Un horodatage fiable (UTC ISO 8601)
- 🔏 Une signature de l’émetteur (ex. Ed25519)
- 🗂️ Des métadonnées optionnelles (nom, propriétaire, tags…)

## Pourquoi DigitalMeve ?
- 🌐 **Universel** et interopérable
- ⏱️ **Rapide** (preuve en < 2 s)
- 🔐 **Sécurisé** (hash + signature)
- 🤝 **Simple** (lisible & vérifiable par machine)

👉 Pour la structure formelle, voir **[Specification](./specification.md)**.  
👉 Pour des cas concrets, voir **[Examples](./examples.md)**.
