"""
DEMO LEVEL 9: Inferencia YOLO (Simulada)
----------------------------------------
Añade: Generación de predicciones complejas (diccionarios).
Acumula: Stream, bucle y condiciones.

DIAGRAMA:
(procesar_frame)
      |
      v
(yolo_inference) -> Genera {'prediccion': {'class': 'Coche', ...}}
      |
      v
(Condition) -> Reacciona a la predicción
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
def procesar_frame(data):
    frame_id, _ = next(data["stream"])
    return {"frame_id": frame_id}


@step(name="yolo_inference")
@to_obj
def yolo_inference(ctx):
    hay_algo = random.random() < 0.5
    if hay_algo:
        pred = {"class": "Peatón", "conf": 0.95}
        print(f"🔍 YOLO: Detectado {pred['class']} ({pred['conf']})")
        return {"detectado": True, "info_ia": pred}
    return {"detectado": False, "info_ia": None}


@step(name="alerta_seguridad")
def alerta_seguridad(data):
    obj = data["info_ia"]["class"]
    print(f"⚠️ ALERTA: {obj} en la trayectoria!")
    return {}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L9", verbose=True)
    pipe.set_steps(
        [
            iniciar_camara,
            For(
                iterations=5,
                steps=[
                    procesar_frame,
                    yolo_inference,
                    Condition(
                        expression="detectado == True", branch_true=[alerta_seguridad]
                    ),
                ],
            ),
        ]
    )
    pipe.run({})
