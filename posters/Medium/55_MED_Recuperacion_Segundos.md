# Medium | Recuperación en Segundos: De "Reprocesar Todo" a "Continuar"

## El Coste de Reiniciar desde Cero
Cada re-ejecución completa de un pipeline largo significa tiempo, cómputo y riesgo de duplicados. En el mundo real, "volver a empezar" es caro.

## wpipe: Continuity por Diseño
Los checkpoints de wpipe permiten recuperar el estado exacto en segundos. No reinicias: **continúas**.

```python
from wpipe import Pipeline, step

@step(name="etl")
def etl(data):
    return {"procesado": len(data)}

pipe = Pipeline(pipeline_name="etl", tracking_db="etl.db")
pipe.set_steps([etl])
pipe.run({"data": [...]})
```

### ¿Por qué en segundos?
- El checkpoint se lee de un SQLite local ultra-rápido.
- El contexto se restaura sin repetir los pasos ya completados.
- El tracker tiene el mapa de qué se hizo y qué falta.

## Conclusión
La recuperación en segundos no es magia: es arquitectura. Y con wpipe, viene de serie.

#Python #Recovery #wpipe #DataEngineering #Resilience