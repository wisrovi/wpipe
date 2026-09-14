# Medium | Estado Persistente: El Bajo el Capó de wpipe

## ¿Por qué tu pipeline debería "recordar"?
La mayoría de scripts no recuerdan nada. Si el proceso se corta, el estado se pierde. Con wpipe, cada paso escribe su estado en un **Tracker SQL local**, de modo que el pipeline siempre sabe dónde quedó.

## Estado que sobrevive a los crash
- **Persistencia total**: cada resultado intermedio queda guardado.
- **Recuperación automática**: al relanzar, wpipe detecta el último checkpoint y continúa.
- **Auditabilidad**: el tracker conserva quién, qué y cuándo.

```python
from wpipe import Pipeline, state

@state(name="ingest")
def ingest(data):
    return {"rows": len(data)}

pipe = Pipeline(pipeline_name="ingest", tracking_db="ingest.db")
pipe.set_steps([ingest])
pipe.run({"data": [...]})
```

## Conclusión
Un pipeline que olvida es un riesgo operativo. Con wpipe, el estado persistente es la base del motor, no un plugin.

#Python #StateManagement #wpipe #Backend #Reliability