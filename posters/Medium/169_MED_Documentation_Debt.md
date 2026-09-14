# Medium | La Deuda de la Documentación: El Coste Oculto de las Docs Manuales

## Todos la Han Visto
El diagrama que ya no coincide con el código. El README que explica un flujo que ya no existe. La wiki que nadie se atreve a tocar. Ese es el "documentation debt": deuda técnica que se paga con confusión.

## La Raíz del Problema
La documentación manual se desincroniza de la realidad. Cada cambio en la lógica requiere un cambio en la doc — y nadie lo hace a tiempo.

## La Solución: Docs Generadas
wpipe genera la documentación de tu pipeline **a partir del código**:
- Diagramas Mermaid automáticos del flujo real.
- Metadata de cada paso (`name`, `version`, retries).
- Trazabilidad desde un tracker SQL persistente.

```python
from wpipe import Pipeline, step

@step(name="transform", version="v1.2")
def transform(data):
    return {"value": data["x"] * 2}

pipe = Pipeline(pipeline_name="docs")
pipe.set_steps([transform])
pipe.run({"x": 21})
```

## Conclusión
La mejor documentación es la que no se mantiene manualmente porque se genera sola. Con wpipe, tu código y tus docs siempre coinciden.

#Documentation #Mermaid #wpipe #Python #TechnicalDebt