---
name: sphinx-docs
version: 1.0.0
description: "Genera documentación Sphinx profesional lista para Read the Docs. USA cuando el usuario mencione 'sphinx', 'readthedocs', 'rtfd', 'API docs', 'generar docs HTML', o 'documentación navegable'."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [sphinx, documentation, html, readthedocs, api-docs]
  requires: [sphinx, sphinx-rtd-theme]
inputs:
  - type: project_path
    description: Ruta del proyecto Python
outputs:
  - type: sphinx_structure
    description: docs/ con estructura Sphinx completa
  - type: html_docs
    description: Documentación HTML compilada
anti_trigger:
  - "Solo quiero PDF"
triggers:
  - "sphinx"
  - "readthedocs"
  - "API docs"
  - "generar docs HTML"
---

# Sphinx Documentation Generator

## Rol

Senior Technical Writer especializado en Sphinx y Read the Docs.

---

## ESTRUCTURA REQUERIDA

```
docs/
├── Makefile              # Required by RTD
├── make.bat             # Windows support
├── requirements.txt      # Documentation deps
└── source/
    ├── conf.py          # Sphinx config
    ├── index.rst        # Main page
    ├── installation.rst
    ├── usage.rst
    ├── api/
    │   └── modules.rst
    ├── tutorials/
    │   ├── index.rst
    │   └── first_steps.rst
    └── _static/
```

---

## COMANDOS

```bash
# Install deps
pip install sphinx sphinx-rtd-theme sphinx-autodoc-typehints

# Generate autodoc
sphinx-apidoc -f -o docs/source/api app/

# Build HTML
cd docs && make html

# Serve locally
cd docs && make html && python -m http.server 8000 -d _build/html
```

---

## .readthedocs.yaml

```yaml
version: 2

build:
  os: ubuntu-22.04
  tools:
    python: "3.11"

sphinx:
  configuration: docs/source/conf.py

python:
  install:
    - requirements: docs/requirements.txt
```

---

## VERIFICACIONES

- [ ] Makefile existe en docs/
- [ ] .readthedocs.yaml en raíz
- [ ] conf.py con sphinx_rtd_theme
- [ ] Author con LinkedIn
- [ ] HTML compilado sin errores
