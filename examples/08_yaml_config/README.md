# Configuracion con YAML

Este modulo contiene ejemplos para cargar configuraciones de archivos YAML y usarlas con pipelines.

## Concepto

Wpipe incluye utilidades para manejar archivos de configuracion YAML:
- **leer_yaml()**: Lee archivos de configuracion YAML
- **escribir_yaml()**: Escribe configuraciones a archivos YAML

Esto permite separar la configuracion del codigo, facilitando:
- Cambios de configuracion sin modificar codigo
- Configuraciones especificas por ambiente
- Reutilizacion de configuraciones

## Funciones Principales

```python
from wpipe.util import leer_yaml, escribir_yaml

config = leer_yaml("config.yaml")
escribir_yaml("config.yaml", {"clave": "valor"})
```

## Estructura de Archivo YAML

```yaml
nombre: mi_servicio
version: v1.0.0
configuracion:
  timeout: 30
  reintentos: 3
  verbose: true
```

## Uso en Pipelines

```python
from wpipe import Pipeline
from wpipe.util import leer_yaml

config = leer_yaml("config.yaml")
pipeline = Pipeline(
    verbose=config.get("configuracion", {}).get("verbose", False)
)
```

## Ejemplos Disponibles

### 01_read_yaml.py
Lectura basica de archivos de configuracion YAML.

```bash
python 01_read_yaml.py
```

### 02_write_yaml.py
Escritura de configuraciones a archivos YAML.

```bash
python 02_write_yaml.py
```

### 03_pipeline_with_config.py
Pipeline que usa configuracion desde archivo YAML.

```bash
python 03_pipeline_with_config.py
```

### 04_complex_config.py
Configuracion compleja con multiples secciones.

```bash
python 04_complex_config.py
```

## Ejecucion de Pruebas

```bash
# Ejecutar todos los ejemplos
pytest yaml_config/ -v

# Ejecutar un ejemplo especifico
python yaml_config/01_read_yaml.py
```
