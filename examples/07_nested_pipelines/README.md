# Pipelines Dentro de Pipelines

Este modulo contiene ejemplos de pipelines anidados, donde un pipeline puede ejecutar otro pipeline como paso.

## Concepto

Un pipeline puede incluir otros pipelines como pasos, permitiendo:
- Composicion de flujos de trabajo complejos
- Reutilizacion de pipelines predefinidos
- Modularidad y organizacion del codigo
- Jerarquias de procesamiento

## Uso Basico

```python
from wpipe import Pipeline

# Crear un sub-pipeline
pipeline1 = Pipeline(verbose=True)
pipeline1.set_steps([(step1, "Paso1", "v1.0")])

# Crear pipeline principal con sub-pipeline anidado
pipeline2 = Pipeline(verbose=True)
pipeline2.set_steps([
    (pipeline1.run, "Pipeline Anidado", "v1.0"),  # Anidar usando .run
    (step2, "Paso2", "v1.0"),
])

resultado = pipeline2.run({"datos": "valor"})
```

## Estructura de Datos

Los datos fluyen automaticamente entre pipelines anidados:
- El resultado de un paso se pasa al siguiente
- Los pipelines anidados reciben los datos del pipeline padre
- Los resultados se acumulan en el estado compartido

## Casos de Uso

1. **Modularidad**: Crear pipelines reutilizables para tareas comunes
2. **Composicion**: Construir pipelines complejos a partir de componentes simples
3. **Abstraccion**: Ocultar detalles de implementacion detras de interfaces simples

## Ejemplos Disponibles

### 01_simple_nested.py
Pipeline anidado simple. Ejemplo basico de como anidar pipelines.

```bash
python 01_simple_nested.py
```

### 02_complex_nested.py
Pipeline anidado complejo. Multiples sub-pipelines con diferentes funciones.

```bash
python 02_complex_nested.py
```

### 03_nested_with_conditions.py
Pipeline anidado con condiciones. Combina anidamiento con Conditional.

```bash
python 03_nested_with_conditions.py
```

### 04_deep_nesting.py
Anidamiento profundo. Pipeline dentro de pipeline dentro de pipeline.

```bash
python 04_deep_nesting.py
```

## Notas Importantes

- Cada sub-pipeline debe crearse una vez y usarse en un solo pipeline padre
- Evitar reutilizar la misma instancia de pipeline en multiples padres
- Los pipelines anidados se ejecutan sincronamente (no en paralelo)
- El estado se comparte entre todos los niveles de anidamiento

## Ejecucion de Pruebas

```bash
# Ejecutar todos los ejemplos
pytest nested_pipelines/ -v

# Ejecutar un ejemplo especifico
python nested_pipelines/01_simple_nested.py
```
