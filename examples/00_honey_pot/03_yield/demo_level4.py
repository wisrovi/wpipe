"""
DEMO LEVEL 4: Configuración con Clases
--------------------------------------
Añade: Uso de Clases como pasos con parámetros (__init__).
Acumula: Paso 1 (encender_motor), Paso 2 (frenos), Paso 3 (validar).

DIAGRAMA:
[Bodega Inicial]
      |
      v
(encender_motor) --> (revisar_frenos) --> (validar_estado)
      |
      v
(ConfigurarGPS @step) -> ¡Recibe el 'destino' como parámetro!
"""

from wpipe import Pipeline, step, to_obj


# Heredados:
def encender_motor(data):
    return {"motor": "ON", "gasolina": 100}


@step(name="revisar_frenos")
def revisar_frenos(data):
    return {"frenos": "OK"}


@step(name="validar_estado")
@to_obj
def validar_estado(ctx):
    print(f"🚀 Coche listo. Gasolina: {ctx.gasolina}%")
    return {"listo": True}


# NUEVO EN L4: Pasos con configuración inicial
@step(name="configurar_gps")
class ConfigurarGPS:
    def __init__(self, destino):
        self.destino = destino

    def __call__(self, data):
        print(f"📍 GPS: Calculando ruta a {self.destino}...")
        return {"destino": self.destino, "distancia": 450}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L4", verbose=True)
    pipe.set_steps(
        [
            encender_motor,
            revisar_frenos,
            validar_estado,
            ConfigurarGPS("Madrid"),  # <--- Pasamos el parámetro aquí
        ]
    )
    pipe.run({})
