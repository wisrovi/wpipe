# Medium | Sin YAML Mágico: La Configuración que se Puede Debuggear

## El Problema del YAML Pesado
Configuraciones gigantes en YAML que "funcionan por magia" son un dolor: no hay tipos, no hay debugging, no hay autocompletado.

## wpipe: Config en Código
La configuración de wpipe vive en Python (opcionalmente con YAML declarativo para parámetros). El resultado: config de verdad, revisable y testeable.

| Aspecto | YAML "mágico" | Config en wpipe |
| :--- | :--- | :--- |
| **Tipos** | Sin validar | Verificados |
| **Debugging** | Difícil | Estándar de Python |
| **Versionado** | Dudoso | Git Flow |

```python
from wpipe import Pipeline, step

@step(name="config")
def config(data):
    return {"factor": data.get("factor", 1)}

pipe = Pipeline(pipeline_name="yml")
pipe.set_steps([config], config_path="pipeline.yml")
```

## Conclusión
La fuente de verdad de tu configuración debe estar en tu repositorio, no en un panel mágico. Con wpipe, es verificable.

#Python #YAML #wpipe #DevOps #Configuration