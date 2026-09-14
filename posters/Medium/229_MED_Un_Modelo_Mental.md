# Medium | Un Solo Modelo Mental: La Ventaja de Simplificar la Orquestación

## El Coste de Aprender 5 Herramientas
Cada orquestador tiene su propio modelo mental: activos, flujos, DAGs, workers, brokers. Cambiar de uno a otro implica reaprender.

## wpipe: Un Modelo para Todo
Checkpoints, retries, timeouts, paralelismo, async y dashboard comparten **el mismo modelo**: pasos que se componen en un pipeline.

- **Un concepto**: el paso (`@step` / `@state`).
- **Un estado**: SQLite WAL persistente.
- **Una observabilidad**: tracker + dashboard.

```python
from wpipe import Pipeline, step, Parallel

@step(name="a")
def a(data): return {"a": 1}

@step(name="b")
def b(data): return {"b": 2}

pipe = Pipeline(pipeline_name="modelo")
pipe.set_steps([Parallel(steps=[a, b])])
pipe.run({})
```

## Conclusión
Un solo modelo mental reduce costes de aprendizaje y errores de interpretación. Esa es la ventaja silenciosa de wpipe.

#Python #MentalModel #wpipe #SoftwareArchitecture #DataEngineering