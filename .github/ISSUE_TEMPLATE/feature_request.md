name: Feature request
description: Proposer une amélioration ou une nouvelle capacité
labels: ["enhancement"]
body:
  - type: textarea
    id: value
    attributes:
      label: Valeur / cas d’usage
      description: Pourquoi est-ce utile pour .meve ?
    validations:
      required: true
  - type: textarea
    id: proposal
    attributes:
      label: Proposition
      placeholder: Décris l’API/CLI/format…
