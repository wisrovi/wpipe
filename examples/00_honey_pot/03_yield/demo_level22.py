"""
DEMO LEVEL 22: Recuperación de Señal (Retries)
----------------------------------------------
Añade: retry_count y retry_delay para fallos intermitentes.
Acumula: Telemetría (L16).

DIAGRAMA:
(conectar_gps) -- [Fallo] -> Espera 0.5s -> Reintento 1
      |--- [Fallo] -> Espera 0.5s -> Reintento 2
      |--- [¡Conectado!] -> Continúa ruta.
"""

import random

from wpipe import Pipeline, step


# NUEVO EN L22: Reintenta hasta 5 veces antes de rendirse
@step(name="conectar_gps", retry_count=10, retry_delay=0.5)
def conectar_gps(data):
    if random.random() < 0.8:  # Simulamos mala cobertura bajo un puente
        print("🛰️ GPS: Buscando señal de satélite...")
        raise ConnectionError("Señal débil")

    print("🛰️ GPS: ¡Posición fijada con éxito!")
    return {"lat": 40.41, "lon": -3.70}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L22_GPS_Recovery", verbose=True)
    pipe.set_steps([conectar_gps])

    print(
        ">>> Iniciando navegación: El sistema se recuperará solo de las pérdidas de señal."
    )
    pipe.run({})
