# Medium | WAL Mode: Por qué SQLite es Suficiente (y el Ecosistema se Equivoca)

## El Mito de "Necesitas Postgres"
Para la mayoría de pipelines, un servidor de base de datos externo es infraestructura innecesaria. SQLite con **Write-Ahead Logging (WAL)** ofrece durabilidad, concurrencia de lecturas y cero configuración.

## Qué aporta WAL en wpipe
- **Escrituras atómicas**: el estado nunca queda a medias.
- **Lecturas simultáneas**: varios pasos paralelos sin corromper el estado.
- **Zero-Config**: un archivo local, sin credenciales ni servidores.

```python
from wpipe import Pipeline, step

@step(name="transform")
def transform(data):
    return {"value": data["x"] * 2}

pipe = Pipeline(pipeline_name="wal_demo")
pipe.set_steps([transform])
pipe.run({"x": 21})
```

## Conclusión
No necesitas un clúster de bases de datos para orquestar datos. WAL + SQLite = robustez de grado industrial con la simplicidad de un archivo.

#SQLite #WAL #Python #wpipe #DataEngineering