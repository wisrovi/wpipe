"""
DEMO LEVEL 2: Metadatos (@step)
-------------------------------
Añade: Uso de @step para dar nombre, versión y trazabilidad a los pasos.
Acumula: Paso 1 (encender_motor).

DIAGRAMA:
[Bodega Vacía]
      |
      v
(encender_motor) ----> [motor: 'ON']
      |
      v
(revisar_frenos @step) -> [motor: 'ON', frenos: 'OK']
"""

from wpipe import Pipeline, step


# Paso heredado del Nivel 1
def encender_motor(data):
    print("🔑 Girando llave: Motor encendido.")
    return {"motor": "ON", "gasolina": 100}


# NUEVO EN L2: @step para mejorar la organización
@step(name="revisar_frenos", version="v1.0")
def revisar_frenos(data):
    print("👟 Probando pedales: Frenos verificados.")
    return {"frenos": "OK"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L2", verbose=True)
    pipe.set_steps([encender_motor, revisar_frenos])
    pipe.run({})
