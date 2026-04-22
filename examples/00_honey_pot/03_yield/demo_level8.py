"""
DEMO LEVEL 8: Ramificaciones (Condition)
----------------------------------------
Añade: Uso de Condition() para ejecutar ramas True/False.
Acumula: Stream de cámara y procesamiento en bucle.

DIAGRAMA:
(procesar_frame)
      |
      v
Condition(¿Obstáculo detectado?)
      |--- [True]  -> (frenar_emergencia)
      |--- [False] -> (acelerar_suave)
"""

import random

import numpy as np

from wpipe import Condition, For, Pipeline, step, to_obj


def simular_video():
    for i in range(10):
        yield i, np.zeros((100, 100, 3))


@step(name="iniciar_camara")
def iniciar_camara(data):
    return {"stream": simular_video()}


@step(name="procesar_frame")
@to_obj
def procesar_frame(ctx):
    try:
        frame_id, _ = next(ctx.stream)
        peligro = random.random() < 0.3
        print(f"🖼️ Frame {frame_id} | Peligro: {peligro}")
        return {"current_frame": frame_id, "obstaculo": peligro}
    except StopIteration:
        return {"error": "Fin"}


@step(name="frenar")
def frenar(data):
    print("🛑 ¡FRENO DE EMERGENCIA ACTIVADO!")
    return {"accion": "Frenando"}


@step(name="acelerar")
def acelerar(data):
    print("🛣️ Carretera libre. Acelerando...")
    return {"accion": "Acelerando"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L8", verbose=True)
    pipe.set_steps(
        [
            iniciar_camara,
            For(
                iterations=5,
                steps=[
                    procesar_frame,
                    Condition(
                        expression="obstaculo == True",
                        branch_true=[frenar],
                        branch_false=[acelerar],
                    ),
                ],
            ),
        ]
    )
    pipe.run({})
