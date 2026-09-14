# Medium | Fallos Transitorios: El Enemigo que se Puede Tolerar

## Los Fallos que no Deberían Tirar tu Pipeline
Un timeout de 2 segundos, una conexión saturada, un rate-limit temporal. Son fallos transitorios: no representan un error real en tu lógica, pero en un script sin retries, matan el job igualmente.

## wpipe: Retries con Pausa Controlada
wpipe define la estrategia de reintentos en dos parámetros y maneja todo el resto.

```python
from wpipe import step, Pipeline

@step(name="api_call", retry_count=3, retry_delay=1)
def api_call(data):
    return {"connected": True}

pipe = Pipeline(pipeline_name="retry")
pipe.set_steps([api_call])
pipe.run({})
```

### Modelo de resiliencia
1. **Reintenta** con pausa controlada ante fallos temporales.
2. **Registra** el error con su contexto en el tracker SQL.
3. **Delega** al checkpoint si el fallo persiste y es crítico.

## Conclusión
Los fallos transitorios son parte de la vida. Que tu arquitectura los **tolere** es una decisión de diseño. Con wpipe, es una línea de código.

#Python #Reliability #wpipe #Backend #Automation