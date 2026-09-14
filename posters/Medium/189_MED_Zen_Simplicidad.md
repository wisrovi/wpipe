# Medium | La Simplicidad es Software: La Filosofía Zen de wpipe

## Menos Código, Más Claridad
La complejidad no es una señal de madurez: es una señal deuda técnica acumulada. Los mejores sistemas son los que hacen mucho con poco.

## wpipe: Zen en la Orquestación
Un pipeline en wpipe es código Python puro, legible y componible.

| Aspecto | Tools complejas | wpipe (Zen) |
| :--- | :--- | :--- |
| **Configuración** | YAML anidado + UI | Python puro |
| **Estado** | Bases externas | SQLite local |
| **Docs** | Manuales obsoletos | Mermaid generado |
| **Setup** | Horas | `pip install` |

```python
from wpipe import Pipeline, step

@step(name="hola")
def hola(data):
    return {"msg": "Hola, " + data["nombre"]}

pipe = Pipeline(pipeline_name="zen")
pipe.set_steps([hola])
pipe.run({"nombre": "Mundo"})
```

## Conclusión
La simplicidad es la máxima sofisticación. wpipe lleva el zen a la orquestación de datos.

#Python #CleanCode #wpipe #Simplicity #SoftwareArchitecture