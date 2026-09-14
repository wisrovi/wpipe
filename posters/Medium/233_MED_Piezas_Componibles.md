# Medium | Piezas Componibles: Pipelines que se Arman como Bloques

## El Monolito de 500 Pasos
Un pipeline gigante es imposible de leer, testear y mantener. La solución no es más coraje: es composición.

## wpipe: Pipelines dentro de Pipelines
Un pipeline puede ser un paso dentro de otro pipeline. Composición clásica aplicada a datos.

```python
from wpipe import Pipeline, step

sub = Pipeline(pipeline_name="sub")
sub.set_steps([paso_a, paso_b])

padre = Pipeline(pipeline_name="padre")
padre.set_steps([
    paso_inicial,
    sub,          # Un pipeline como paso
    paso_final
])
```

### Los beneficios
- **Reutilización**: un sub-pipeline vive en un módulo y se usa en 10 flujos.
- **Aislamiento**: cada pieza se testea por separado.
- **Claridad**: el padre describe el negocio; los hijos, la implementación.

## Conclusión
Piezas pequeñas, bien probadas, orquestadas a cualquier escala. Esa es la composición que no falla.

#Python #Composition #wpipe #SoftwareArchitecture #DataEngineering