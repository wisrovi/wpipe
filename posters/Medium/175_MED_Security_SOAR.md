# Medium | El Stack de Seguridad Lean: SOAR Ligero vs. Herramientas Pesadas

## El Problema con el SOAR Tradicional
Las plataformas SOAR prometen orquestar la respuesta a incidentes, pero a menudo vienen con licencias caras, agentes pesados y una caja negra de lógica propietaria.

## wpipe: Orquestación de Seguridad en Python
La respuesta a incidentes es, en el fondo, un pipeline de datos: detectar, enriquecer, decidir, responder. wpipe lo orquesta con menos de 50MB de RAM.

- **Ligero**: <50MB de RAM, corre donde las suites SOAR no pueden.
- **Pythonico**: cada playbook es código auditable, versionable y testeable.
- **Resiliente**: checkpoints SQLite WAL para no perder eventos críticos.

```python
from wpipe import Pipeline, step

@step(name="enriquecer_ioc")
def enriquecer_ioc(data):
    return {"ioc": data["hash"], "score": 9}

pipe = Pipeline(pipeline_name="soar")
pipe.set_steps([enriquecer_ioc])
pipe.run({})
```

## Conclusión
La seguridad no debería depender de cajas negras caras. wpipe da a los equipos de SecOps la potencia de orquestación con la transparencia del código.

#Cybersecurity #SOAR #wpipe #Python #SecOps