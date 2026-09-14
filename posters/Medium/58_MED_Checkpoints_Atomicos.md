# Medium | Checkpoints Atómicos: La Garantía de que el Estado Nunca Queda a Medias

## Atómico no es una Palabra de Moda
Un checkpoint atómico significa que cada escritura de estado es todo-o-nada. Si el proceso se corta a mitad de una escritura, el estado anterior permanece intacto.

## Cómo lo logra wpipe
La combinación de **SQLite** con **modo WAL** hace que los checkpoints sean atómicos y durables.

- **Escritura completa o ninguna**: sin estados corruptos.
- **Crash-safe**: ante un corte eléctrico, el buffer WAL se recupera en el próximo arranque.
- **Consistente bajo paralelismo**: hilos y procesos escriben sin corromper el estado.

```python
from wpipe import Pipeline, step

@step(name="atomic_step")
def atomic_step(data):
    return {"ok": data["value"]}

pipe = Pipeline(pipeline_name="atomic")
pipe.set_steps([atomic_step])
pipe.run({"value": 42})
```

## Conclusión
Si tu pipeline guarda estado, haz que sea atómico. wpipe te da esa garantía de forma nativa.

#SQLite #WAL #wpipe #DataEngineering #Reliability