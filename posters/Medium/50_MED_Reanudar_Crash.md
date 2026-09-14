# Medium | Reanudar Después de un Crash: El Superpoder de los Checkpoints

## El Escenario que Todos Conocemos
Son las 4 AM. Tu pipeline lleva 6 horas procesando datos. Un microservicio externo se cae. Resultado: proceso muerto, progreso perdido, y tú reiniciando desde el paso 1.

## wpipe: Reanudar, no Reiniciar
wpipe detecta el fallo, preserva el contexto en el checkpoint y al reanudar **hidrata el estado exacto** del último paso completado.

- Se acabaron las re-ejecuciones completas.
- Se acabó el reprocesado manual de datos.
- Se acabó el "rezo a las 3 AM".

```python
from wpipe import Pipeline, step

@step(name="heavy")
def heavy(data):
    return {"ok": True}

pipe = Pipeline(pipeline_name="crash_resume", tracking_db="resume.db")
pipe.set_steps([heavy])
# El próximo run retoma desde el último checkpoint
pipe.run({})
```

## Conclusión
La pregunta no es "si" habrá un crash, sino "cuánto pierdes" cuando ocurre. Con wpipe, la respuesta es: nada.

#Python #Resilience #wpipe #Checkpoints #DataPipelines