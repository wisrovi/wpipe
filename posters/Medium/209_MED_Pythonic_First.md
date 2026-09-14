# Medium | Python-First: La Orquestación que Respeta tu Ecosistema

## El Mundo Gira en Python
Si tus datos, tus librerías y tu equipo viven en Python, la orquestación también debería hacerlo. No deberías cambiar de idioma para orquestar.

## wpipe: Python-First de Verdad
- **Configuración en Python**: nada de DSLs propietarios.
- **Integración natural**: cualquier librería de PyPI es parte del pipeline.
- **Un solo stack**: tu lógica, tu testing, tu orquestador en el mismo idioma.

```python
from wpipe import Pipeline, step
import pandas as pd

@step(name="analisis")
def analisis(data):
    df = pd.DataFrame(data["rows"])
    return {"media": df["value"].mean()}

pipe = Pipeline(pipeline_name="py_first")
pipe.set_steps([analisis])
pipe.run({"rows": [...]})
```

## Conclusión
Python-First no es un slogan: es arquitectura. Con wpipe, tu pipeline habla el idioma de tu base de código.

#Python #Pandas #wpipe #DataScience #DataEngineering