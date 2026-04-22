"""
DEMO LEVEL 10: El Parabrisas Inteligente (HUD)
---------------------------------------------
Añade: Dibujado de realidad aumentada sobre los frames de la cámara.
Acumula: Sistema de Visión (L9) y Cámara (L6).

DIAGRAMA:
(Cámara) -> (Sistema Visión ADAS) -> [Objeto detectado]
      |                                    |
      +------------> (Dibujar HUD) <-------+
                        |
                        v
              [Frame con Marcadores]
"""

import random

import cv2
import numpy as np

from wpipe import For, Pipeline, step, to_obj


@step(name="activar_vision_adas")
@to_obj
def adas_vision(ctx):
    # El sistema de asistencia detecta si hay un coche delante
    distancia = random.randint(10, 100)
    return {"vehiculo_delante": True, "distancia_m": distancia}


@step(name="render_hud")
@to_obj
def render_hud(ctx):
    # Simulamos el parabrisas inteligente dibujando sobre el frame
    frame_id, frame = next(ctx.stream)
    color = (0, 255, 0) if ctx.distancia_m > 30 else (0, 0, 255)

    # Dibujamos la info en el 'parabrisas' (frame)
    cv2.putText(
        frame,
        f"OBJ: COCHE | DIST: {ctx.distancia_m}m",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
    )

    print(f"🖥️  HUD [Frame {frame_id}]: Visualizando vehículo a {ctx.distancia_m}m")
    return {"visualizacion": frame}


if __name__ == "__main__":
    from demo_level6 import iniciar_camara

    pipe = Pipeline(pipeline_name="Viaje_L10_HUD", verbose=True)
    pipe.set_steps([iniciar_camara, For(iterations=3, steps=[adas_vision, render_hud])])
    pipe.run({})
