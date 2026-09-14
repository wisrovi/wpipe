# Medium | Minimal Setup: De Cero a Pipeline Industrial en Minutos

## El Freno Número Uno: El Setup
Antes de escribir tu primera transformación, la mayoría de soluciones te piden: Docker, un broker, una base de datos, credenciales... El setup mata la motivación.

## wpipe: Un Solo Comando
```bash
pip install wpipe
```
Y ya está. Sin servidores, sin contenedores obligatorios, sin configuración de red.

```python
from wpipe import Pipeline, step

@step(name="primer_paso")
def primer_paso(data):
    return {"listo": True}

pipe = Pipeline(pipeline_name="primer")
pipe.set_steps([primer_paso])
pipe.run({})
```

### El resultado
- **Time-to-first-pipeline**: minutos, no horas.
- **Curva de onboarding**: cero fricción para nuevos devs.
- **Iteración instantánea**: edit, run, debug.

## Conclusión
Un setup mínimo no es comodidad: es velocidad de desarrollo. Con wpipe, el pipeline industrial empieza tras un `pip install`.

#Python #Onboarding #wpipe #DevExperience #ZeroConfig