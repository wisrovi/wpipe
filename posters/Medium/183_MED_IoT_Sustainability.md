# Medium | El Edge Verde: Reducir la Huella de Carbono con Pipelines Ligeros

## Cada Byte Tiene un Coste de CO2
Las decisiones de arquitectura afectan directamente las emisiones: más RAM y más servidores significan más energía. La computación pesada es cara para el planeta y para tu presupuesto.

## wpipe: Menos RAM = Menos Energía = Menos Carbono
- **<50MB de RAM**: una fracción del consumo de los orquestadores tradicionales.
- **Local-first**: sin brokers ni bases externas que mantener encendidas.
- **Edge-ready**: corre en dispositivos de bajo consumo como Raspberry Pi.

| Métrica | wpipe | Orquestadores tradicionales |
| :--- | :--- | :--- |
| RAM | <50MB | 500MB - 2GB+ |
| Energía | Baja | Alta |
| Infra extra | Ninguna | Servidores/Brokers |

```python
from wpipe import Pipeline, step

@step(name="edge")
def edge(data):
    return {"value": data["x"]}

pipe = Pipeline(pipeline_name="green_edge")
pipe.set_steps([edge])
pipe.run({"x": 1})
```

## Conclusión
La eficiencia no es solo una métrica técnica: es una responsabilidad ambiental. Elegir herramientas ligeras es Green-IT en acción.

#GreenIT #Sustainability #wpipe #Python #EdgeComputing