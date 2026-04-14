---
name: documentation
version: 1.0.0
description: "Genera documentación completa: Sphinx (HTML) + LaTeX (PDF) + Technical Whitepaper. USA los PNGs de readme-makefile. Invoca sphinx-docs antes de PDF. USA cuando el usuario mencione 'generar PDF', 'documentación LaTeX', 'whitepaper', 'technical docs', o 'generar documentación completa'."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [documentation, latex, pdf, whitepaper, technical]
  requires: [texlive, pandoc, sphinx]
inputs:
  - type: project_path
    description: Ruta del proyecto
  - type: doc_type
    description: Tipo de documentación (pdf, html, whitepaper, all)
outputs:
  - type: pdf_document
    description: PDF compilado
  - type: html_docs
    description: Documentación Sphinx HTML
  - type: whitepaper
    description: Technical Whitepaper 40-60 páginas
anti_trigger:
  - "Solo quiero README"
  - "No necesito PDF"
triggers:
  - "generar PDF"
  - "documentación LaTeX"
  - "whitepaper"
  - "generar documentación completa"
  - "technical docs"
---

# Documentation Generator

## Rol

Senior Technical Writer & Systems Architect.

---

## FLUJO DE TRABAJO

```
1. Si es PDF → Invocar readme-makefile primero
2. Invocar sphinx-docs para HTML
3. Generar LaTeX con PNGs de Excalidraw
4. Compilar PDF
```

---

## Paso 0: readme-makefile (SIEMPRE PRIMERO)

Cuando el usuario pida un PDF, SIEMPRE invocar `readme-makefile` primero:

```bash
# El agente debe ejecutar readme-makefile para generar:
# - README.md
# - docs/diagrams/*.excalidraw
# - docs/diagrams/*.png (renderizados)
```

---

## Paso 1: sphinx-docs (PARA HTML)

Invocar `sphinx-docs` para generar documentación HTML:

```bash
# Ejecutar skill sphinx-docs
# Genera: docs/ con estructura Sphinx completa
# - docs/source/conf.py
# - docs/source/index.rst
# - docs/Makefile
# - etc.
```

---

## Paso 2: LaTeX/PDF

### Preámbulo CRÍTICO

Ver `references/latex-preamble.tex` para el preámbulo exacto.

### Reglas

| Regla | Detalle |
|-------|---------|
| Fuentes | `\usepackage{helvet}` + `\usepackage{courier}` |
| Títulos | `\sffamily` en todos |
| Imágenes | PNGs en `sources/` |

### Integración de PNGs

```latex
\chapter{Architecture}
\section{System Overview}
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.9\textwidth]{sources/system-architecture.png}
    \caption{System Architecture}
\end{figure}
```

---

## Paso 3: TECHNICAL WHITEPAPER

### Estructura

Ver `references/whitepaper-template.tex` para template completo.

### Secciones obligatorias

- Executive Summary
- Architecture Blueprint
- Risk Matrix
- Bibliography (APA)

---

## DEPENDENCIAS ENTRE SKILLS

```
documentation
     │
     ├──→ readme-makefile (genera PNGs de Excalidraw)
     │
     ├──→ sphinx-docs (genera HTML Sphinx) ← SE INVOCA
     │
     └──→ LaTeX → PDF
```

---

## Referencias

| Archivo | Contenido |
|---------|-----------|
| `references/latex-preamble.tex` | Preámbulo LaTeX exacto |
| `references/whitepaper-template.tex` | Template de whitepaper |
| `sphinx-docs/` | Skill para Sphinx HTML |

---

## About the Author

**wisrovi**
- LinkedIn: https://www.linkedin.com/in/wisrovi-rodriguez/
- GitHub: https://github.com/wisrovi
- DockerHub: https://hub.docker.com/u/wisrovi
- PyPI: https://pypi.org/search/?q=wisrovi
- Email: wisrovi.rodriguez@gmail.com
