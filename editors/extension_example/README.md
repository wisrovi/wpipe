# Extension Example Project

Este proyecto es un ejemplo de extensión para un sistema de tuberías de estados (pipeline) usando la librería `wpipe`.

## Requisitos

- [Conda](https://docs.conda.io/en/latest/) instalado.
- Entorno `cv` configurado con `wpipe` v2.3.8 y sus dependencias.

### Dependencias Necesarias

```bash
pip install wpipe==2.3.8 wpipe-steps==0.105.0 wredis==0.9.6 psutil pytest pytest-cov
```

## Instalación

1.  Activar el entorno:
    ```bash
    conda activate cv
    ```
2.  Instalar dependencias y aplicar parches necesarios para la compatibilidad de `wpipe-steps`:
    ```bash
    # (Opcional) Ejecutar el script de prueba para verificar el entorno
    python test_extension.py
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
- Monitorización de recursos (CPU/RAM).

## Pruebas

Siguiendo las directrices del proyecto, se utiliza `pytest` para las pruebas unitarias.

Para ejecutar los tests localmente:
```bash
conda run -n cv pytest tests/
```

Para ejecutar los tests en Docker:
```bash
./run_tests_docker.sh
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
4.  **Parches de Compatibilidad (wpipe-steps)**:
    - Se creó el archivo `decorators.py` faltante en `wpipe_steps.core`.
    - Se eliminaron las restricciones de métodos abstractos en `BaseStep` para permitir la instanciación de pasos pre-construidos.
    - Se corrigieron importaciones en `test_extension.py` y se vaciaron archivos `__init__.py` problemáticos en el paquete instalado.
5.  **Dependencias Actualizadas**: Se instalaron `wredis` v0.9.6 y `psutil` para asegurar el correcto funcionamiento de los pasos de Redis y la monitorización de recursos.
