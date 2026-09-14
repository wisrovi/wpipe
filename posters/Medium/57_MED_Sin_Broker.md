# Medium | Sin Broker: Orquestación que no Depende de Redis ni RabbitMQ

## El Peso Invisible del Broker
Redis o RabbitMQ son soluciones serias... para problemas grandes. Para la mayoría de pipelines, un broker introduce latencia, una pieza más que puede caerse y configuración compleja.

## wpipe: Broker-less por Diseño
wpipe gestiona el estado de las tareas directamente en **SQLite WAL**, sin intermediarios.

- **Menos latencia**: la ejecución es directa, no pasa por colas.
- **Menos fricción**: sin Redis que instalar, configurar y monitorear.
- **Menos superficie de ataque**: una pieza menos crítica en tu stack.

```python
from wpipe import Pipeline, state

@state(name="tarea_async")
def tarea_async(data):
    return {"done": True}

pipe = Pipeline(pipeline_name="nol_broker")
pipe.set_steps([tarea_async])
pipe.run({})
```

## Conclusión
A veces la solución más robusta es la que elimina piezas, no la que añade más. Con wpipe, olvídate del broker.

#Python #Celery #wpipe #Backend #ZeroInfra