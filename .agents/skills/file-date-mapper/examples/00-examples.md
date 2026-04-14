# File Date Mapper Examples

## Example 1: CSV Output

```csv
path_original,fecha_creacion,fecha_edicion,en_rango_fechas,path_destino
project/docs/manual.pdf,2025-06-15T10:30:00,2025-06-20T14:45:00,TRUE,evidencias/docs/manual.pdf
project/src/main.py,2025-06-18T09:00:00,2025-06-22T16:20:00,TRUE,evidencias/src/main.py
project/old/config.txt,2024-01-10T08:00:00,2024-01-10T08:00:00,FALSE,
project/README.md,2025-07-01T12:00:00,2025-12-15T11:30:00,TRUE,evidencias/README.md
```

## Example 2: Script Usage

```bash
# Basic usage
python map_files.py \
    --source ./project \
    --dest ./evidencias \
    --start 2025-05-01 \
    --end 2026-01-31 \
    --output file_mapping.csv

# Output
📂 Analyzing: ./project
📅 Range: 2025-05-01 to 2026-01-31
📁 Output: ./evidencias

✅ Complete!
   Total files: 45
   In range: 32
   CSV: file_mapping.csv
```

## Example 3: Directory Structure Result

```
project/
├── docs/
│   ├── manual.pdf        → evidencias/docs/manual.pdf
│   └── guide.pdf        → evidencias/docs/guide.pdf
├── src/
│   ├── main.py          → evidencias/src/main.py
│   └── utils.py         → evidencias/src/utils.py
└── old/
    └── old_file.txt     (not moved - outside range)

evidencias/
├── docs/
│   ├── manual.pdf
│   └── guide.pdf
├── src/
│   ├── main.py
│   └── utils.py
└── README.md
```

## Example 4: Generated Mapping Report

```markdown
# File Date Mapping Report

**Source:** ./project  
**Destination:** ./evidencias  
**Date Range:** 2025-05-01 to 2026-01-31  
**Generated:** 2026-03-24

## Summary

| Metric | Count |
|--------|-------|
| Total Files | 45 |
| In Range | 32 |
| Outside Range | 13 |
| Copied | 32 |

## Files by Month

| Month | Count |
|-------|-------|
| May 2025 | 5 |
| June 2025 | 8 |
| July 2025 | 6 |
| August 2025 | 4 |
| September 2025 | 3 |
| October 2025 | 2 |
| November 2025 | 2 |
| December 2025 | 2 |
| January 2026 | 0 |

## Outside Range Files

| Path | Last Modified |
|------|---------------|
| old/config.txt | 2024-01-10 |
| archive/data.zip | 2023-11-15 |
| backup/settings.json | 2023-08-20 |
```
