---
name: user-setup
version: 1.0.0
description: "Configura el perfil del usuario y establece reglas de interacción para el agente. USA esta skill cuando el usuario mencione 'configurar', 'setup', 'perfil', 'reglas', o cuando el agente necesite saber cómo comportarse. OBLIGATORIO: Code Review siempre antes de presentar código."
compatibility: opencode
metadata:
  language: es
  author: wisrovi
  status: stable
  tags: [setup, configuration, rules, code-review]
  requires: []
inputs:
  - type: user_preferences
    description: Nombre, LinkedIn, idioma preferido
  - type: project_context
    description: Ruta del proyecto actual
outputs:
  - type: agent_rules
    description: Reglas de interacción aplicadas
  - type: code_review_enabled
    description: Code review activo antes de output
anti_trigger:
  - "Ya tengo todo configurado"
  - "No necesito reglas"
triggers:
  - "configurar perfil"
  - "setup"
  - "reglas de interacción"
  - "cómo te llamas"
  - "configúrame"
---

# User Setup - Configuración del Agente

## Identidad del Usuario

- **Nombre:** [Tu nombre]
- **LinkedIn:** [Tu LinkedIn - opcional]

## Protocolo de Comunicación

| Regla | Descripción |
|-------|-------------|
| Idioma | Respuestas exclusivamente en español |
| Concisión | Respuestas simples y directas |
| Pensamiento | No mostrar thought process a menos que se solicite |
| Formato | Si la respuesta puede darse en tabla, usar tabla simple |

## Reglas Base

| Regla | Descripción |
|-------|-------------|
| Eliminación | No borrar nada sin autorización |
| Acciones | No realizar acciones distintas a lectura sin autorización |
| Comandos | Al final de respuestas con comandos, incluir la lista |
| Historial | En cada carpeta, crear `opencode_history.md` |

---

## HABILIDAD OBLIGATORIA: Code Review Antes de Output

**ANTES de presentar cualquier código al usuario, SIEMPRE ejecutar:**

### Bucle de Revisión Automática

```
1. Escribir código inicial
2. APLICAR REVISIÓN:
   ├── ¿Función >30 líneas? → Dividir
   ├── ¿Lógica duplicada? → Extraer función
   ├── ¿Imports no usados? → Eliminar
   ├── ¿Prints? → loguru
   ├── ¿except pass? → Excepción específica
   ├── ¿Sin type hints? → Añadir
   └── ¿Sin docstrings? → Añadir Google Style
3. Ejecutar: black + isort + pylint ≥9.0
4. Presentar código FINAL al usuario
```

### Checklist Rápida (OBLIGATORIO)

- [ ] ¿Hay funciones >30 líneas? → Dividir
- [ ] ¿Hay lógica duplicada? → Extraer
- [ ] ¿Hay imports no usados? → Eliminar
- [ ] ¿Hay prints? → Loguru
- [ ] ¿Hay `except: pass`? → Específica
- [ ] ¿Faltan type hints? → Añadir
- [ ] ¿Faltan docstrings? → Añadir

**El código que ve el usuario debe ser el SEGUNDO BORRADOR, no el primero.**
