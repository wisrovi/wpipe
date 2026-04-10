---
name: readme-makefile
version: 1.0.0
description: "Genera README.md profesional + Makefile completo + Diagramas Excalidraw PNG. USA esta skill cuando el usuario mencione 'crear README', 'generar makefile', 'makefile', 'documentación de proyecto', 'README', o 'dame un README'. Combina README, Mermaid, Excalidraw PNGs y Makefile en un solo workflow."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [documentation, readme, makefile, excalidraw, diagrams]
  requires: [pandoc, excalidraw]
inputs:
  - type: project_path
    description: Ruta del proyecto
  - type: project_name
    description: Nombre del proyecto (opcional, detectar del directorio)
outputs:
  - type: readme_md
    description: README.md completo
  - type: makefile
    description: Makefile con todos los targets
  - type: excalidraw_pngs
    description: PNGs de diagramas en docs/diagrams/
anti_trigger:
  - "Solo quiero el código"
  - "No necesito documentación"
triggers:
  - "crear README"
  - "genera makefile"
  - "documentación"
  - "makefile"
  - "dame un README"
  - "generar docs"
---

# README & Makefile Generator

## Rol

Principal Technical Writer & Software Architect.

---

## FLUJO DE TRABAJO

```
1. Generar README.md profesional
2. Crear diagramas Excalidraw + PNGs
3. Crear Makefile completo
4. (Opcional) Generar extra_readmes/
```

---

## PARTE 1: README.md

### Estructura Obligatoria

```
README.md
├── Title + Badges
├── Quick Start
├── Features
├── Architecture (Mermaid)
├── Technical Stack
├── Installation
├── Configuration
├── Usage
├── Testing
├── Contributing
├── License
└── Author
```

### Comandos de Generación

```bash
# README básico
python .agents/skills/readme-makefile/scripts/generate_readme.py --project .

# Con análisis de código
python .agents/skills/readme-makefile/scripts/generate_readme.py --project . --analyze
```

---

## PARTE 2: EXCALIDRAW DIAGRAMS

### Setup (solo una vez)

```bash
cd .agents/skills/excalidraw-diagram/references
uv sync
uv run playwright install chromium
```

### Diagramas Requeridos

| # | Archivo | Descripción |
|---|---------|-------------|
| 1 | `system-architecture.excalidraw` | Vista general componentes |
| 2 | `data-flow.excalidraw` | Flujo de datos |
| 3 | `component-interaction.excalidraw` | Interacción módulos |

### Renderizado

```bash
make diagrams-render
# O manualmente:
cd .agents/skills/excalidraw-diagram/references
uv run python render_excalidraw.py docs/diagrams/system-architecture.excalidraw \
    --output docs/diagrams/system-architecture.png --scale 2
```

---

## PARTE 3: MAKEFILE

### Targets Obligatorios

| Target | Descripción |
|--------|-------------|
| `help` | Mostrar ayuda |
| `install` | Dependencias |
| `lint` | Pylint ≥9.5 |
| `format` | isort + black |
| `security` | bandit |
| `test` | pytest ≥85% |
| `diagrams` | Crear dir diagramas |
| `diagrams-render` | Render PNGs |
| `docs` | Sphinx HTML |
| `clean` | Limpiar |

### Template Completo

Ver `references/makefile-template.mk`

---

## PARTE 4: EXTRA_DOCS (Opcional)

Para proyectos complejos, generar `extra_readmes/`:

```
extra_readmes/
├── 01-architecture-backend.md
├── 02-communication-flow.md
├── 03-data-diagrams.md
├── 04-security-hardening.md
└── 05-deployment-ops.md
```

---

## VERIFICACIONES

- [ ] README.md con todas las secciones
- [ ] Mermaid en sección Architecture
- [ ] 3 PNGs de Excalidraw en docs/diagrams/
- [ ] Makefile con todos los targets
- [ ] Sección Author obligatoria

---

## Referencias

| Archivo | Contenido |
|---------|-----------|
| `references/readme-sections.md` | Templates de cada sección |
| `references/makefile-template.mk` | Makefile completo |
| `references/excalidraw-colors.md` | Paleta de colores |
