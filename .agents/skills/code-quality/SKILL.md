---
name: code-quality
version: 1.0.0
description: "Audita código Python completamente: Pylint ≥9.0, tests con coverage ≥85%, reportes HTML/PDF profesionales. USA esta skill cuando el usuario mencione 'auditar código', 'quality', 'coverage', 'tests', 'pylint', 'pytest coverage', o 'generar reporte de calidad'. Genera REPORT.md, REPORT.html y REPORT.pdf."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [quality, testing, coverage, pylint, pytest, reports]
  requires: [pylint, pytest, pytest-cov, bandit, black, isort]
inputs:
  - type: project_path
    description: Ruta del proyecto Python a auditar
  - type: coverage_target
    description: Meta de coverage (default: 85%)
outputs:
  - type: report_md
    description: REPORT.md con métricas completas
  - type: report_html
    description: REPORT.html profesional
  - type: report_pdf
    description: REPORT.pdf (opcional)
  - type: coverage_html
    description: htmlcov/ con coverage interactivo
anti_trigger:
  - "Solo quiero ver el código"
  - "No necesito reportes"
triggers:
  - "auditar código"
  - "quality audit"
  - "coverage"
  - "pytest"
  - "pylint"
  - "generar reporte"
  - "test coverage"
---

# Code Quality - Automated Excellence Audit

## Rol

Ingeniero de Calidad de Código (CQE).

---

## FLUJO DE TRABAJO

```
1. Análisis del código
2. Aplicar calidad: black + isort + pylint ≥9.0
3. Seguridad: bandit (cero hallazgos altos)
4. Tests: ≥85% coverage
5. Generar reportes con scripts/
```

---

## FASE I: CALIDAD DE CÓDIGO

### Comandos obligatorios

```bash
# Formateo
isort app/
black app/

# Análisis
pylint --disable=import-error,no-member,no-name-in-module app/ --output-format=text > pylint_report.txt

bandit -r app/ -f screen
```

### KPIs

| KPI | Meta |
|-----|------|
| Pylint Score | ≥9.0/10.0 |
| Bandit | 0 High/Critical |
| Estilo | PEP 8 + Black |

---

## FASE II: TESTS (COBERTURA ≥85%)

```bash
pytest tests/ \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-branch \
    --cov-config=.coveragerc \
    > pytest_output.txt 2>&1
```

### Scripts de ayuda

```bash
# Generar reporte completo (markdown + HTML + PDF)
python .agents/skills/code-quality/scripts/generate_report.py

# Solo coverage analysis
python .agents/skills/code-quality/scripts/analyze_coverage.py --target 85
```

---

## FASE III: GENERAR REPORTES

### Opción 1: Script automatizado (RECOMENDADO)

```bash
cd .agents/skills/code-quality/scripts
python generate_report.py --project . --output ../
```

Esto genera:
- `REPORT.md` - Reporte en Markdown
- `REPORT.html` - Reporte HTML profesional
- `coverage/` - Coverage report interactivo

### Opción 2: Manual

1. Leer `references/html-template.html` para template
2. Leer `references/pylint-rules.md` para reglas
3. Leer `references/coverage-tips.md` para tips de coverage

---

## SALIDA ESPERADA

```
project/
├── REPORT.md           # Reporte Markdown
├── REPORT.html         # Reporte HTML
├── REPORT.pdf         # Reporte PDF (opcional)
├── pylint_report.txt  # Output de pylint
├── pytest_output.txt  # Output de pytest
└── htmlcov/          # Coverage HTML
```

---

## VERIFICACIONES

- [ ] Pylint ≥9.0
- [ ] Bandit sin issues altos
- [ ] Coverage ≥85%
- [ ] black + isort aplicados
- [ ] REPORT.html generado

---

## Referencias

| Archivo | Contenido |
|---------|-----------|
| `references/pylint-rules.md` | Reglas detalladas de pylint |
| `references/coverage-tips.md` | Tips para aumentar coverage |
| `references/html-template.html` | Template del reporte HTML |
| `scripts/generate_report.py` | Script para generar reportes |
| `scripts/analyze_coverage.py` | Script para analizar coverage |
