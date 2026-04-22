"""
DEMO LEVEL 36: Bitácora del Vehículo (YAML)
------------------------------------------
Añade: Persistencia de la bodega de datos en archivos YAML.
Acumula: Todo el historial del viaje.

DIAGRAMA:
(Viaje Finalizado) -> [Bodega] -> (escribir_yaml) -> [bitacora.yaml]
      |
(Nuevo Viaje) <---- (leer_yaml) <----- [bitacora.yaml]
"""

import os

from wpipe import Pipeline, step
from wpipe.util import escribir_yaml, leer_yaml


@step(name="generar_bitacora")
def generar_bitacora(data):
    # Guardamos los datos finales del viaje para la siguiente sesión
    datos_finales = {
        "odometro": 450.5,
        "fuel_restante": 15,
        "ultima_posicion": "Valencia",
        "errores_detectados": 0,
    }
    path = "output/bitacora_viaje.yaml"
    os.makedirs("output", exist_ok=True)
    escribir_yaml(path, datos_finales)
    print(f"📄 Bitácora guardada en {path}. Datos listos para el próximo arranque.")
    return {"path_bitacora": path}


@step(name="leer_bitacora_previa")
def leer_bitacora(data):
    # Simulamos el arranque de mañana leyendo los datos de hoy
    historial = leer_yaml(data["path_bitacora"])
    print(
        f"📥 Bitácora recuperada: El coche estaba en {historial['ultima_posicion']} con {historial['fuel_restante']}% de fuel."
    )
    return {"historial": historial}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Logbook_System_L36", verbose=True)
    pipe.set_steps([generar_bitacora, leer_bitacora])
    pipe.run({})
