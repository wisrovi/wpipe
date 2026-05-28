# Extension Example Project

Este proyecto es un ejemplo de extensión para un sistema de tuberías de estados (pipeline) usando la librería `wpipe`.

## Requisitos

- [Conda](https://docs.conda.io/en/latest/) instalado.
- Entorno `cv` configurado con `wpipe` y sus dependencias.

## Instalación

```bash
conda activate cv
# Las dependencias ya deberían estar en el entorno 'cv'
```

## Ejecución del Pipeline Principal

Para ejecutar el script de ejemplo:

```bash
conda run -n cv python test_extension.py
```

Este script ejecuta un pipeline complejo que incluye:
- Pasos secuenciales y condicionales.
- Bucles `For` iterativos.
- Ejecución en paralelo de pasos y sub-pipelines.
- Captura de errores centralizada.

## Pruebas

Siguiendo las directrices del proyecto, se utiliza `pytest` para las pruebas unitarias.

Para ejecutar los tests:
```bash
conda run -n cv pytest tests/
```

### Coverage

Para calcular la cobertura del código:
```bash
conda run -n cv pytest --cov=. tests/
```

## Estructura del Proyecto

- `test_extension.py`: Punto de entrada principal que define y ejecuta el pipeline.
- `state_pipe.py`: Define `pipe_2`, un sub-pipeline utilizado dentro del pipeline principal.
- `error_capture.py`: Contiene la lógica para capturar y mostrar alertas del sistema en caso de fallos.
- `state*.py`: Implementaciones individuales de cada estado del pipeline.
- `output/`: Directorio donde se guardan las bases de datos de seguimiento (`tracking.db`).

## Correcciones Realizadas

1.  **Tracker Inicializado**: Se habilitó `tracking_db` en `state_pipe.py` para evitar errores de `NoneType` al acceder al tracker.
2.  **Serialización (Pickle)**: Se eliminó el decorador `@to_obj` en `AdvancedStep` que causaba errores de serialización con bloqueos de hilos.
3.  **Conflictos de DB**: Se asignó una base de datos independiente a `pipe_2` para evitar bloqueos de transacciones SQLite durante la ejecución paralela.
