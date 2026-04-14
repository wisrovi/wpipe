# Document to Markdown Examples

## Example 1: DOCX Conversion

```bash
# Basic conversion
pandoc "document.docx" -t markdown -o "document.md"

# With images extracted
pandoc "document.docx" \
    -t markdown \
    -o "document.md" \
    --extract-media=./images \
    --wrap=preserve

# GitHub Flavored Markdown
pandoc "document.docx" -t gfm -o "document.md" --standalone
```

## Example 2: Excel to Markdown

```python
# examples/excel_to_md.py
import pandas as pd

def excel_to_markdown(excel_path, output_path):
    xl = pd.ExcelFile(excel_path)
    with open(output_path, 'w') as f:
        for sheet in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet)
            f.write(f"## {sheet}\n\n")
            f.write(df.to_markdown(index=False))
            f.write("\n\n")

excel_to_markdown("data.xlsx", "data.md")
```

### Output:

```markdown
## Sales Q1

| Product | Revenue | Units |
|---------|---------|-------|
| A | 1000 | 50 |
| B | 2000 | 100 |

## Sales Q2

| Product | Revenue | Units |
|---------|---------|-------|
| A | 1500 | 75 |
| B | 2500 | 125 |
```

## Example 3: Batch Conversion Script

```python
# examples/batch_convert.py
import os
import subprocess
from pathlib import Path

CONVERTERS = {
    '.docx': 'pandoc "{input}" -t markdown -o "{output}" --wrap=preserve',
    '.odt': 'pandoc "{input}" -t markdown -o "{output}"',
    '.pdf': 'pdftotext "{input}" "{output}"',
}

def convert_file(input_path):
    ext = input_path.suffix.lower()
    if ext not in CONVERTERS:
        return None, f"Unsupported: {ext}"
    
    output = input_path.with_suffix('.md')
    if output.exists():
        return None, "Skipped (exists)"
    
    cmd = CONVERTERS[ext].format(input=input_path, output=output)
    try:
        subprocess.run(cmd, shell=True, check=True)
        return output, "Success"
    except subprocess.CalledProcessError as e:
        return None, str(e)

for f in Path('.').rglob('*'):
    if f.is_file() and f.suffix.lower() in CONVERTERS:
        result, msg = convert_file(f)
        status = "✅" if result else "⚠️"
        print(f"{status} {f.name}: {msg}")
```

## Example 4: Conversion Report

```markdown
# Conversion Report

| Metric | Value |
|--------|-------|
| Total | 15 |
| Exitosos | 12 |
| Omitidos | 2 |
| Fallidos | 1 |

### Archivos Fallidos

| Archivo | Error |
|---------|-------|
| corrupted.docx | Invalid DOCX format |
```

## Example 5: PDF Text Extraction

```bash
# Extract text from PDF
pdftotext document.pdf output.txt

# Extract with layout preserved
pdftotext -layout document.pdf output.txt

# Extract first 10 pages
pdftotext -f 1 -l 10 document.pdf output.txt
```
