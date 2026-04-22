"""
DEMO LEVEL 1: El Inicio (Funciones Simples)
-------------------------------------------
Añade: Creación de Pipeline y ejecución de una función secuencial.

DIAGRAMA:
[Bodega Vacía]
      |
      v
(encender_motor) --> [motor: 'ON', gasolina: 100]
"""

from wpipe import Pipeline


def encender_motor(data):
    print("🔑 Girando llave: Motor encendido.")
    return {"motor": "ON", "gasolina": 100}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L1", verbose=True)
    pipe.set_steps([encender_motor])
    pipe.run({})
