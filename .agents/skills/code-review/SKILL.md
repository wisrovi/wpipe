---
name: code-review
version: 1.0.0
description: "Revisa código Python automáticamente ANTES de presentarlo. Refactoriza, mejora calidad y genera Security Report estilo pentest. USA esta skill cuando: el usuario pida 'revisar código', 'analizar código', mencione 'seguridad', 'vulnerabilidades', o siempre ANTES de presentar código. MIENTRAS el agente escriba código, debe aplicar esta skill."
compatibility: opencode
metadata:
  language: en
  author: wisrovi
  status: stable
  tags: [code-review, security, quality, python, bandit, safety]
  requires: [pylint, bandit, safety]
inputs:
  - type: code_snippet_or_files
    description: Código a revisar (snippet o archivos)
  - type: project_path
    description: Ruta del proyecto (opcional)
outputs:
  - type: refactored_code
    description: Código mejorado y refactorizado
  - type: security_report
    description: SECURITY_REPORT.md con análisis de vulnerabilidades
  - type: checklist_results
    description: Checklist de revisión completado
anti_trigger:
  - "Ya revisé el código"
  - "Solo quiero ver el código sin revisar"
triggers:
  - "revisar código"
  - "analiza este código"
  - "code review"
  - "seguridad"
  - "vulnerabilidades"
  - "bandit"
  - "analiza seguridad"
---

# Code Review - Automated Pre-Output Review

## Propósito

El código que ve el usuario debe ser el **SEGUNDO BORRADOR**, no el primero.

---

## CHECKLIST DE REVISIÓN (EJECUTAR ANTES DE OUTPUT)

```
┌─────────────────────────────────────────┐
│  1. ¿Función >30 líneas? → Dividir      │
│  2. ¿Lógica duplicada? → Extraer        │
│  3. ¿Imports no usados? → Eliminar      │
│  4. ¿Prints? → loguru                  │
│  5. ¿except pass? → Excepción específica │
│  6. ¿Sin type hints? → Añadir          │
│  7. ¿Sin docstrings? → Añadir           │
│  8. ¿Bandit tiene issues? → Corregir    │
│  9. ¿Safety tiene alerts? → Actualizar │
│ 10. ¿Pylint ≥9.0? → Verificar          │
└─────────────────────────────────────────┘
```

### Comandos de verificación

```bash
# Seguridad
bandit -r app/ -f screen
safety check --json

# Calidad
isort --check-only .
black --check .
pylint --disable=import-error,no-member,no-name-in-module app/
```

---

## SECURITY REPORT

Ver `references/security-report-template.md` para template completo del reporte estilo pentest.

### Estructura del reporte

- Executive Summary con métricas
- Vulnerabilidades por severidad (Critical/High/Medium/Low)
- Proof of Concept
- Dependency Analysis
- Recommendations

---

## ESTÁNDARES DE CÓDIGO

Ver `references/coding-standards.md` para reglas detalladas:

- Nomenclatura
- Docstrings (Google Style)
- Type hints
- Exception handling
- Logging con loguru

---

## About the Author

**[Author]**  
AI Solutions Architect & Technology Evangelist
