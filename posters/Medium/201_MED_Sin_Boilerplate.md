# Medium | Sin Boilerplate: La Configuración que no Es un Proyecto en sí

## El Antipatrón del Over-Configuration
Levantar un orquestador "serio" suele implicar: configurar el scheduling, definir el broker, crear los workers, conectar la UI... antes de escribir tu primera línea de lógica.

## wpipe: Menos Setup, Más Resultado
El setup de wpipe es cero: `pip install` y a trabajar.

- **Sin contenedores** obligatorios: corre como librería.
- **Sin brokers**: el estado vive en SQLite local.
- **Sin UI obligatoria**: el dashboard es opcional y local.

```python
from wpipe import Pipeline, step

@step(name="run")
def run(data):
    return {"ok": True}

pipe = Pipeline(pipeline_name="no_boilerplate")
pipe.set_steps([run])
pipe.run({})
```

## Conclusión
El boilerplate es deuda técnica disfrazada de infraestructura. Con wpipe, tu pipeline empieza donde debe: en la lógica.

#Python #ZeroConfig #wpipe #DevOps #Backend