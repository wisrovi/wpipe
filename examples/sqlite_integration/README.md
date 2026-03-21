# Persistencia con SQLite

Este modulo contiene ejemplos para guardar inputs y outputs de pipelines en una base de datos SQLite.

## Concepto

Wpipe integra soporte para SQLite permitiendo:
- Guardar automaticamente inputs de cada ejecucion
- Guardar outputs resultantes del procesamiento
- Almacenar detalles adicionales
- Exportar datos a CSV o DataFrames
- Consultar resultados guardados

## Clases Principales

### Wsqlite
Wrapper con context manager para uso sencillo:
```python
from wpipe.sqlite import Wsqlite

with Wsqlite(db_name="resultados.db") as db:
    db.input = {"datos": "entrada"}
    resultado = pipeline.run({"datos": "entrada"})
    db.output = resultado
```

### SQLite
Clase base con operaciones avanzadas:
```python
from wpipe.sqlite import Wsqlite
from wpipe.sqlite.Sqlite import SQLite

with SQLite(db_name="resultados.db") as db:
    df = db.export_to_dataframe()
    db.export_to_dataframe(save_csv=True, csv_name="resultados.csv")
```

## Estructura de la Base de Datos

| Campo | Tipo | Descripcion |
|-------|------|-------------|
| id | INTEGER | Identificador unico (auto-increment) |
| input | TEXT | JSON con datos de entrada |
| output | TEXT | JSON con resultados |
| details | TEXT | Metadatos adicionales |
| datetime | TEXT | Timestamp de creacion |

## Ejemplos Disponibles

### 01_save_results.py
Guardar resultados de pipeline en SQLite.

```bash
python 01_save_results.py
```

### 02_read_results.py
Leer y consultar resultados guardados.

```bash
python 02_read_results.py
```

### 03_export_csv.py
Exportar datos a archivos CSV.

```bash
python 03_export_csv.py
```

### 04_advanced_queries.py
Consultas avanzadas y filtrado.

```bash
python 04_advanced_queries.py
```

## Uso Basico

```python
from wpipe import Pipeline
from wpipe.sqlite import Wsqlite

def paso_procesamiento(data: dict) -> dict:
    return {"resultado": data.get("x", 0) * 2}

pipeline = Pipeline()
pipeline.set_steps([(paso_procesamiento, "Proceso", "v1.0")])

# Guardar con Wsqlite
with Wsqlite(db_name="mi_pipeline.db") as db:
    db.input = {"x": 10}
    resultado = pipeline.run({"x": 10})
    db.output = resultado
    print(f"ID del registro: {db.id}")
```

## Ejecucion de Pruebas

```bash
# Ejecutar todos los ejemplos
pytest sqlite_integration/ -v

# Ejecutar un ejemplo especifico
python sqlite_integration/01_save_results.py
```
