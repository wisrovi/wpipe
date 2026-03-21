name: Bug Report
description: Report a bug in wpipe
labels: bug
body:
  - type: textarea
    id: description
    attributes:
      label: Description
      description: A clear description of the bug
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: Steps to reproduce the bug
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What you expected to happen
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened
    validations:
      required: true

  - type: dropdown
    id: python-version
    attributes:
      label: Python Version
      options:
        - 3.9
        - 3.10
        - 3.11
        - 3.12
        - 3.13
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant Log Output
      description: Paste any relevant log output or error messages

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Add any other context about the problem
