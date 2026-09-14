# Medium | Mantenibilidad: El Pipeline que tu "Yo del Futuro" te Agradecerá

## Código que se Abandona vs. Código que se Mantiene
La mayoría de pipelines mueren de "deuda repartida": lógica duplicada en scripts, documentación obsoleta y miedo a tocar el flujo.

## wpipe: Diseñado para Ser Mantenido
- **Componentes reutilizables**: crea pasos una vez, úsalos en todos tus flujos.
- **Auto-documentación**: Mermaid se genera desde el código.
- **Testeable**: cada paso es una función de Python pura.

```python
from wpipe import Pipeline, step

@step(name="normalizar")
def normalizar(data):
    return [d.lower() for d in data["textos"]]

pipe = Pipeline(pipeline_name="mant")
pipe.set_steps([normalizar])
pipe.run({"textos": [...]})
```

## Conclusión
Un pipeline que no se puede mantener se convierte en legacy en meses. Con wpipe, la mantenibilidad es una propiedad del diseño, no un esfuerzo extra.

#Maintainability #Python #wpipe #CleanCode #SoftwareEngineering