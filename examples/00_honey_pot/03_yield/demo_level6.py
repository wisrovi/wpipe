"""
DEMO LEVEL 6: Generadores (Stream de Datos)
-------------------------------------------
Añade: Uso de generadores (yield) para simular flujo de cámara.
Acumula: Preparación del coche (Niveles 1-5).

DIAGRAMA:
[Configuración Inicial]
      |
      v
(Preparar Coche) -> [motor, gps, clima]
      |
      v
(iniciar_camara) -> Devuelve un Generador (yield)
      |
      v
[Bodega con 'stream': <generator object>]
"""

import cv2
import numpy as np

from wpipe import Pipeline, step


# Heredados:
def preparar(data):
    return {"motor": "ON", "gps": "Valencia"}


# NUEVO EN L6: El flujo de datos
def simular_video():
    for i in range(10):
        # Simulamos una imagen negra con el ID del frame
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        yield i, img


@step(name="iniciar_camara")
def iniciar_camara(data):
    print("📸 Cámara frontal: Activada.")
    # El generador se guarda en la bodega para ser consumido después
    return {"stream": simular_video()}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L6", verbose=True)
    pipe.set_steps([preparar, iniciar_camara])
    pipe.run({})
