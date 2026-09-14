# Medium | Menos es Mejor: El Caso Contra los Orquestadores Pesados

## La Falsa Economía del Gigante
"Usar Airflow porque es lo estándar" es una frase que esconde un coste: infraestructura enorme para pipelines que caben en una librería.

## wpipe: Potencia Industrial, Huella Mínima
- **<50MB de RAM**: corre donde otros orquestadores ni arrancan.
- **Milisegundos de latencia**: sin overhead de scheduler.
- **Zero infra externa**: SQLite local, no Postgres ni Redis.

```python
from wpipe import Pipeline, step

@step(name="ligero")
def ligero(data):
    return {"value": data["x"] + 1}

pipe = Pipeline(pipeline_name="ligero")
pipe.set_steps([ligero])
pipe.run({"x": 1})
```

## Conclusión
Menos recursos, menos piezas, menos coste. La eficiencia no es rendirse: es diseñar mejor.

#GreenIT #Python #wpipe #Efficiency #SoftwareArchitecture