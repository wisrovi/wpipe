# Plan: Dashboard - Vista por Versiones (Code Hash)

## Por qué se quiere implementar

Cuando desarrollamos el sistema de **deduplicación por hash** (code_hash), descubrimos que:

1. **El mismo código = mismo hash** - Ejecuciones repetidas del mismo pipeline generan el mismo `code_hash`, pero diferentes `pipeline_id`.

2. **El dashboard mostraba todo separado** - Sin agrupamiento, cada ejecución aparecía como un pipeline nuevo, imposible distinguir ejecuciones del mismo código vs código diferente.

3. **No había historia** - No podías ver cuántas veces se ejecutó el mismo pipeline, ni comparar rendimiento entre ejecuciones del mismo código.

4. **Confusión visual** - Si ejecutabas 4 veces el mismo pipeline, veías 4 entradas separadas sin relación aparente.

**Solución:** Agrupar por `code_hash` para que el usuario vea:
- Las versiones únicas de código (una por hash)
- Al expandir, todas sus ejecuciones con grafos individuales
- Historial de rendimiento por versión

---

## Cómo se debería implementar el sistema de deduplicación

### Concepto: Code Hash = Identidad del Pipeline

Cada pipeline se identifica por un **hash único** calculado a partir de:
- Nombre del pipeline
- Versión del pipeline
- Contenido de archivos locales (states, funciones custom)
- Estructura de steps (tipos, nombres, versiones)
- Pipelines anidados (referenciados por su hash)

### Flujo de registro

```
Pipeline.run()
    ↓
register_pipeline()
    ↓
_calcular_code_hash(name, version, steps)
    ↓
code_hash = "sha256:abc123..."
    ↓
¿Existe configs/{code_hash}.yaml?
    ├── SÍ → Reutilizar, mostrar "Reusing existing pipeline version"
    └── NO → Crear nuevo YAML, nuevo registro en pipeline_versions
    ↓
Crear NUEVO pipeline_id (cada ejecución única)
    ↓
Guardar en pipelines (con su config_yaml = configs/{code_hash}.yaml)
```

### Archivos involucrados

```
configs/
├── sha256:abc123...yaml  ← Config del pipeline (nombre, version, steps)
├── sha256:def456...yaml  ← Otro pipeline
└── ...
```

### Cambios en la librería (wpipe)

1. **`tracker.py`**:
   - `_compute_code_hash()` → calcula hash único
   - `find_by_code_hash()` → busca YAML existente
   - `_generate_yaml_config()` → crea YAML con metadata

2. **`pipe.py`**:
   - `add_state()` → añade state al pipeline
   - `add_pipeline()` → añade pipeline anidado
   - `add_condition()` → añade condición
   - `code_hash` property → hash calculado después de ejecutar

3. **DB (pipeline_versions)**:
   - `code_hash` (único) → `pipeline_id` (primera ejecución)
   - Relación: múltiples `pipelines.id` → mismo `pipeline_versions.code_hash`

### Resultado esperado

- Misma ejecución repetida → reutiliza YAML, muestra "reusing"
- Código diferente → nuevo hash, nuevo YAML, nuevo pipeline
- Dashboard agrupa por hash → historia completa por versión

---

## Objetivo

Implementar una visualización de pipelines agrupados por `code_hash` donde:
- Cada "versión" única (mismo código) es un ítem clickeable
- Al expandir, muestra todas las ejecuciones con sus grafos individuales
- Sin superposición de nodos

---

## Problema Actual

Cuando se ejecuta el mismo pipeline múltiples veces:
- Se crean múltiples `pipeline_id` únicos
- El dashboard muestra cada ejecución como un pipeline separado
- No hay forma de ver que son ejecuciones del mismo código

---

## Solución: Opción A

Vista tipo acordeón donde:
```
┌─────────────────────────────────────────────────┐
│  Pipeline Versions (agrupado por code_hash)     │
├─────────────────────────────────────────────────┤
│  honey_pot_reporter v1.0.0        [4 ejecuciones]│
│  ├── PIPE-001  ✓  1.2s  15:45:32               │
│  ├── PIPE-002  ✓  1.1s  15:44:50               │
│  ├── PIPE-003  ✓  1.3s  15:44:12               │
│  └── PIPE-004  ✗  0.9s  15:43:45               │
├─────────────────────────────────────────────────┤
│  honey_pot_inference v1.0.0       [3 ejecuciones]│
│  └── expandir...                               │
└─────────────────────────────────────────────────┘
```

Al clickear una ejecución → muestra su grafo individual (sin superposición)

---

## Archivos a Modificar

| Archivo | Cambios |
|---------|---------|
| `wpipe/tracking/tracker.py` | +2 funciones |
| `wpipe/dashboard/main.py` | +2 endpoints |
| `wpipe/dashboard/templates/tabs/pipelines.html` | Vista HTML nueva |
| `wpipe/dashboard/static/dashboard.js` | +3 funciones JS |
| `wpipe/dashboard/static/styles.css` | Estilos para versiones |

---

## 1. Backend: tracker.py

### Nueva función: `get_pipeline_versions()`

Agrupa ejecuciones por `code_hash` y cuenta estadísticas.

```sql
SELECT 
    pv.code_hash,
    pv.name,
    pv.version,
    COUNT(DISTINCT p.id) as execution_count,
    MAX(p.started_at) as last_executed,
    SUM(CASE WHEN p.status = 'completed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
    AVG(p.total_duration_ms) as avg_duration_ms
FROM pipeline_versions pv
LEFT JOIN pipelines p ON p.config_yaml LIKE '%' || pv.code_hash || '%'
GROUP BY pv.code_hash
ORDER BY last_executed DESC
```

### Nueva función: `get_executions_by_hash(code_hash)`

Obtiene todas las ejecuciones de una versión específica.

```sql
SELECT * FROM pipelines 
WHERE config_yaml LIKE '%{code_hash}%'
ORDER BY started_at DESC
```

---

## 2. Backend: main.py

### Nuevos endpoints:

```python
@app.get("/api/pipeline-versions")
async def get_pipeline_versions():
    """Lista de versiones únicas agrupadas por code_hash."""

@app.get("/api/pipeline-versions/{code_hash}/executions")
async def get_executions_by_hash(code_hash: str):
    """Ejecuciones específicas de una versión."""
```

---

## 3. Frontend: dashboard.js

### Nuevas funciones:

```javascript
// Carga versiones agrupadas desde la API
async function loadPipelineVersions()

// Renderiza lista de versiones expandibles
function renderVersionList(versions)

// Expande una versión para mostrar sus ejecuciones
async function expandVersion(code_hash)

// Selecciona una ejecución individual y muestra su grafo
async function selectExecution(pipeline_id)
```

---

## 4. Frontend: HTML

Nuevo tab `pipelines.html` con estructura para lista de versiones.

---

## 5. Backend: main.py (actualizado)

Endpoints nuevos:
- `GET /api/pipeline-versions` → lista versiones únicas
- `GET /api/pipeline-versions/{code_hash}/executions` → ejecuciones de una versión

---

## Flujo de Datos

```
User carga dashboard
    ↓
GET /api/pipeline-versions
    ↓
Respuesta: [{code_hash, name, version, execution_count, ...}]
    ↓
Renderizar lista de versiones
    ↓
User clickea "expandir" en una versión
    ↓
GET /api/pipeline-versions/{code_hash}/executions
    ↓
Respuesta: [{pipeline_id, status, duration, ...}]
    ↓
Renderizar ejecuciones anidadas
    ↓
User clickea ejecución individual
    ↓
GET /api/pipelines/{pipeline_id}/graph
    ↓
Renderizar grafo (sin superposición)
```

---

## Estado de Implementación

- [x] Diseñar plan
- [x] Backend: `tracker.py` - funciones agregadas
- [x] Backend: `main.py` - endpoints agregados
- [ ] Frontend: `pipelines.html` - en progreso
- [ ] Frontend: `dashboard.js` - pendiente
- [ ] Frontend: `styles.css` - pendiente
- [ ] Pruebas y ajustes finales

---

## Notas

- El `code_hash` se busca en `config_yaml` usando LIKE con el hash
- La tabla `pipeline_versions` ya existe con `code_hash` único
- Cada ejecución mantiene su `pipeline_id` único para referenciar su grafo
