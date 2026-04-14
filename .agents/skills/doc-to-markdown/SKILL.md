---
name: doc-to-markdown
version: 1.0.0
description: "Convierte documentos (DOCX, PDF, Excel, ODT) a Markdown. USA cuando el usuario mencione 'convertir a markdown', 'DOCX a md', 'PDF a texto', 'Excel a tabla', 'migrar documentos', o 'extraer contenido de documento'."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [conversion, markdown, pandoc, documents]
  requires: [pandoc, pdftotext]
inputs:
  - type: input_files
    description: Archivos a convertir (.docx, .pdf, .xlsx, .odt)
  - type: output_format
    description: Formato de salida (markdown, gfm)
outputs:
  - type: markdown_files
    description: Archivos .md generados
  - type: extracted_images
    description: Imágenes extraídas (si aplica)
anti_trigger:
  - "Ya tengo el markdown"
triggers:
  - "convertir a markdown"
  - "DOCX a md"
  - "PDF a texto"
  - "migrar documentos"
---

# Document to Markdown Conversion

## Rol

Ingeniero de Automatización de Documentos auto-suficiente.

---

## HERRAMIENTAS REQUERIDAS

```bash
# Sistema
sudo apt update && sudo apt install -y pandoc poppler-utils

# Python
pip install pandas openpyxl odfpy python-docx
```

---

## CONVERSIÓN POR TIPO

| Tipo | Comando |
|------|---------|
| **DOCX** | `pandoc archivo.docx -t markdown -o archivo.md --wrap=preserve` |
| **PDF** | `pdftotext archivo.pdf archivo.txt` |
| **Excel** | Script Python (ver abajo) |
| **ODT** | `pandoc archivo.odt -t markdown -o archivo.md` |

### DOCX Completo (con imágenes)

```bash
pandoc "documento.docx" \
    -t markdown \
    -o "documento.md" \
    --extract-media=./images \
    --wrap=preserve \
    --standalone
```

---

## BUCLE DE CONVERSIÓN

```bash
# Batch conversion
python .agents/skills/doc-to-markdown/scripts/batch_convert.py --source ./docs
```

---

## REPORTE FINAL

```markdown
# Conversion Report

| Métrica | Valor |
|---------|-------|
| Total | X |
| Exitosos | X |
| Omitidos | X |
| Fallidos | X |
```

---

## VERIFICACIONES

- [ ] Herramientas instaladas
- [ ] Imágenes extraídas correctamente
- [ ] Estructura de encabezados preservada
- [ ] Reporte generado
