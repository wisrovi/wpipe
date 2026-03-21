name: Feature Request
description: Suggest a new feature for wpipe
labels: enhancement
body:
  - type: textarea
    id: feature-description
    attributes:
      label: Feature Description
      description: A clear description of the feature you'd like to see
    validations:
      required: true

  - type: textarea
    id: problem
    attributes:
      label: Problem Statement
      description: What problem does this feature solve?

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should this feature work?

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Any alternative solutions you've considered

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Add any other context or screenshots
