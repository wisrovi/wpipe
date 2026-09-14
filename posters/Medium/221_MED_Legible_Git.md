# Medium | Legible en Git: Por qué tu Pipeline Debería Vivir en un Repositorio

## El Día que Necesitas el "Blame"
¿Quién cambió la lógica de ese paso? ¿Cuándo se introdujo el bug? Si tu pipeline vive en una UI, estas preguntas no tienen respuesta.

## wpipe: Pipelines en Git, con Todo lo que Eso Implica
- **Ctrl+Z del equipo**: cualquier cambio es reversible.
- **Review real**: los cambios pasan por Pull Request.
- **Auditoría**: el historial de Git es tu bitácora.

```python
from wpipe import Pipeline, step

@step(name="legible")
def legible(data):
    return {"ok": data["id"]}

pipe = Pipeline(pipeline_name="git")
pipe.set_steps([legible])
pipe.run({"id": 1})
```

### El principio
Tu pipeline es un activo de software. Un activo de software se versiona, se revisa y se audita. Punto.

## Conclusión
Si tu lógica de negocio vive encadenada en una herramienta visual, estás perdiendo el mayor aliado del ingeniero: Git.

#Git #Versioning #wpipe #Python #SoftwareEngineering