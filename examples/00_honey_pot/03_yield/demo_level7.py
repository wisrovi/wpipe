"""
DEMO LEVEL 7: Bucles (For)
--------------------------
Añade: Uso de For() para procesar frames repetidamente.
Acumula: Paso de cámara (Nivel 6).

DIAGRAMA:
(iniciar_camara) --> [stream: <generador>]
      |
      v
   For(10 iteraciones) {
      (procesar_frame) -> Consume 'next(ctx.stream)'
   }
"""

import cv2
import numpy as np

from wpipe import For, Pipeline, step, to_obj


# Heredado del L6:
def simular_video():
    for i in range(10):
        yield i, np.zeros((100, 100, 3))


@step(name="iniciar_camara")
def iniciar_camara(data):
    return {"stream": simular_video()}


# NUEVO EN L7: Consumo de frames en bucle
@step(name="procesar_frame")
@to_obj
def procesar_frame(ctx):
    # Extraemos el siguiente frame del generador guardado en la bodega
    try:
        frame_id, frame = next(ctx.stream)
        print(f"🖼️ Procesando frame: {frame_id}")
        return {"current_frame": frame_id}
    except StopIteration:
        return {"error": "Stream finalizado"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L7", verbose=True)
    pipe.set_steps(
        [
            iniciar_camara,
            # Ejecutamos el paso de procesamiento 5 veces
            For(iterations=5, steps=[procesar_frame]),
        ]
    )
    pipe.run({})
