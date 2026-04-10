---
name: excalidraw-diagram
version: 1.0.0
description: "Genera diagramas Excalidraw profesionales con PNGs exportados usando Playwright. USA cuando el usuario mencione 'diagrama excalidraw', 'generar diagrama PNG', 'arquitectura visual', 'flowchart', o 'generar PNG de diagrama'."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [diagrams, excalidraw, png, architecture, visualization]
  requires: [playwright]
inputs:
  - type: diagram_type
    description: Tipo de diagrama (architecture, flow, sequence)
  - type: elements
    description: Elementos del diagrama (cajas, flechas, texto)
outputs:
  - type: excalidraw_json
    description: Archivo .excalidraw con JSON
  - type: png_image
    description: Imagen PNG renderizada
anti_trigger:
  - "Solo quiero texto"
triggers:
  - "diagrama excalidraw"
  - "generar diagrama PNG"
  - "arquitectura visual"
  - "flowchart"
---

# Excalidraw Diagram Creator

## Setup

```bash
cd .agents/skills/excalidraw-diagram/references
uv sync
uv run playwright install chromium
```

---

## DIAGRAMAS A GENERAR

| # | Archivo | Descripción |
|---|---------|-------------|
| 1 | `system-architecture.excalidraw` | Vista general componentes |
| 2 | `data-flow.excalidraw` | Flujo de datos |
| 3 | `component-interaction.excalidraw` | Interacción módulos |

---

## RENDERIZADO

```bash
cd .agents/skills/excalidraw-diagram/references
uv run python render_excalidraw.py \
    docs/diagrams/system-architecture.excalidraw \
    --output docs/diagrams/system-architecture.png \
    --scale 2
```

---

## PALETA DE COLORES

| Componente | strokeColor | backgroundColor |
|------------|-------------|-----------------|
| Frontend | `#0891b2` | `#cffafe` |
| Backend | `#1e40af` | `#dbeafe` |
| Database | `#7c3aed` | `#ede9fe` |
| External | `#ea580c` | `#ffedd5` |
| Start | `#059669` | `#d1fae5` |
| Error | `#dc2626` | `#fee2e2` |

---

## VERIFICACIONES

- [ ] Archivo .excalidraw creado con JSON válido
- [ ] PNG renderizado correctamente
- [ ] Sin elementos solapados
- [ ] Flechas conectan elementos correctos
