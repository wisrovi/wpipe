# Medium | El Decorador @step: Toda la Potencia en una Línea

## La Orquestación no Debería Invadir tu Código
Las herramientas pesadas te obligan a reescribir tu lógica para adaptarla a su modelo. wpipe hace lo contrario: tu función se convierte en un paso con un decorador.

## @step: Tu Lógica, Tu Pipeline
```python
from wpipe import step, Pipeline

@step(name="ingest", retry_count=3)
def ingest(data):
    return {"ingested": len(data)}

pipe = Pipeline(pipeline_name="deco")
pipe.set_steps([ingest])
pipe.run({"data": [...]})
```

### Lo que ganas con un decorador
- **Resiliencia**: retries, timeouts y checkpoints sin tocar tu función.
- **Observabilidad**: cada run queda en el tracker SQL.
- **Claridad**: la intención del paso queda explícita en el código.

## Conclusión
El decorador `@step` convierte cualquier función Python en un paso industrial. Menos boilerplate, más lógica de negocio.

#Python #Decorators #wpipe #Backend #CleanCode