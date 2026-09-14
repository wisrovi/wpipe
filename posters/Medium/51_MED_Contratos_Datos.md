# Medium | Contratos de Datos: Validación en el Borde, no al Final

## El Error Clásico de Producción
Un campo llega como `str` donde esperabas `int`. Ese dato atraviesa 5 pasos sin que nadie se dé cuenta... hasta que explota en el último. Ese escenario cuesta horas de debugging.

## PipelineContext: Tu Contrato de Datos
Con wpipe defines el contrato del flujo y la validación ocurre automáticamente al borde del pipeline.

```python
from wpipe import Pipeline, step, PipelineContext

class Orden(PipelineContext):
    id: int
    total: float

@step(name="validar")
def validar(orden: Orden):
    return {"importe": orden.total}

pipe = Pipeline(pipeline_name="ordenes")
pipe.set_steps([validar])
pipe.run({"id": 1, "total": 99.90})
```

### Beneficios
- **Tipos verificados contra el esquema**, paso a paso.
- **Errores tempranos**: fallas en el borde, no en producción.
- **Auto-documentación**: el contrato describe la forma de los datos.

## Conclusión
Datos correctos a la entrada = pipeline predecible a la salida. Deja de confiar en "el que envía, envía bien".

#Python #TypeSafety #DataEngineering #wpipe #CleanCode