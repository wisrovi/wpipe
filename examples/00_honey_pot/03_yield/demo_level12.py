"""
DEMO LEVEL 12: Visión Estereoscópica (Parallel)
-----------------------------------------------
Añade: Procesamiento paralelo de la cámara Frontal y Trasera.
Acumula: Sistemas ADAS (L10).

DIAGRAMA:
(procesar_viaje)
      |
   Parallel(sensores) {
      |-- (camara_frontal) -> [Detecciones delante]
      |-- (camara_trasera) -> [Detecciones detrás]
   }
      |
      v
(fusion_datos) -> [Mapa 360°]
"""

import time

from wpipe import Parallel, Pipeline, step, to_obj


@step(name="ojo_frontal")
def ojo_frontal(d):
    time.sleep(0.1)
    print("🔭 Mirando adelante: Carretera despejada.")
    return {"frontal": "Libre"}


@step(name="ojo_trasero")
def ojo_trasera(d):
    time.sleep(0.1)
    print("🔭 Mirando atrás: Vehículo aproximándose.")
    return {"trasera": "Coche a 20m"}


@step(name="fusion_360")
@to_obj
def fusion_360(ctx):
    print(f"🤖 IA Fusión: Delante={ctx.frontal} | Detrás={ctx.trasera}")
    return {"entorno_seguro": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L12_Vision360", verbose=True)
    pipe.set_steps(
        [Parallel(steps=[ojo_frontal, ojo_trasera], max_workers=2), fusion_360]
    )
    pipe.run({})
