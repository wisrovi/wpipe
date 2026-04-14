---
name: file-date-mapper
version: 1.0.0
description: "Mapea archivos por fecha de creación y mueve a carpeta evidencias. Genera CSV de mapeo. USA cuando el usuario mencione 'mapear archivos por fecha', 'evidencias', 'organizar por fecha', 'mover archivos', o 'archivos por fecha'."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [files, dates, organization, evidence, scripts]
  requires: []
inputs:
  - type: source_directory
    description: Directorio con archivos a mapear
  - type: date_range
    description: Rango de fechas (YYYY-MM-DD a YYYY-MM-DD)
  - type: destination
    description: Carpeta destino (default: evidencias/)
outputs:
  - type: csv_mapping
    description: file_mapping.csv con mapeo completo
  - type: organized_files
    description: Archivos movidos a evidencias/
anti_trigger:
  - "Ya tengo los archivos organizados"
triggers:
  - "mapear archivos por fecha"
  - "evidencias"
  - "organizar por fecha"
  - "mover archivos"
---

# File Date Mapper - Evidence Collection Script

## Objetivo

Analizar archivos por fecha y organizar en carpeta evidencias.

---

## COMANDO

```bash
python .agents/skills/file-date-mapper/scripts/map_files.py \
    --source ./project \
    --dest ./evidencias \
    --start 2025-05-01 \
    --end 2026-01-31 \
    --output file_mapping.csv
```

---

## CSV DE SALIDA

```csv
path_original,fecha_creacion,fecha_edicion,en_rango_fechas,path_destino
project/src/main.py,2025-06-15T10:30:00,2025-06-20T14:45:00,TRUE,evidencias/src/main.py
project/old.txt,2024-01-10T08:00:00,2024-01-10T08:00:00,FALSE,
```

---

## ESTRUCTURA RESULTANTE

```
evidencias/
├── docs/
│   ├── manual.pdf
│   └── guide.pdf
├── src/
│   ├── main.py
│   └── utils.py
└── README.md
```

---

## VERIFICACIONES

- [ ] CSV generado con todas las columnas
- [ ] Archivos dentro del rango movidos
- [ ] Estructura de carpetas preservada
- [ ] Archivos fuera del rango NO movidos
