name: Bug report
description: Signaler un problème ou un échec de vérification .meve
labels: ["bug"]
body:
  - type: textarea
    id: desc
    attributes:
      label: Description
      description: Que s'est-il passé ? Quel résultat attendais-tu ?
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Étapes pour reproduire
      description: Commandes, fichiers .meve, contexte…
      placeholder: |
        1. …
        2. …
  - type: input
    id: version
    attributes:
      label: Version DigitalMeve
      placeholder: "ex: 1.6.0"
  - type: dropdown
    id: py
    attributes:
      label: Version Python
      options: ["3.10", "3.11", "3.12"]
