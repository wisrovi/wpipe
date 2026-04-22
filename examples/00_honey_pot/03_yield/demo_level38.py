"""
DEMO LEVEL 38: Gestión Híbrida de Recursos
------------------------------------------
Añade: Combinación de hilos y procesos para máxima eficiencia.
Acumula: Paralelismo Total (L25).

DIAGRAMA:
[Hilos]   -> (Sensores de Aire, Temperatura, Humedad) -> Ligeros
[Procesos] -> (IA de Reconocimiento de Objetos 4K)    -> Pesados
"""

from wpipe import Pipeline, step, ParallelO
import time


@step(name="ia_pesada_4k")
def ia_pesada(d):
    time.sleep(0.3)
    return {"video_analizado": "OK"}


@step(name="sensor_ligero_aire")
def sensor_ligero(d):
    return {"calidad_aire": "Excelente"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Hybrid_Power_L38", verbose=True)

    pipe.set_steps(
        [
            # 1. Usamos procesos para la carga pesada de vídeo
            Parallel(steps=[ia_pesada] * 2, use_processes=True, max_workers=2),
            # 2. Usamos hilos para sensores que no consumen apenas CPU
            Parallel(steps=[sensor_ligero] * 4, use_processes=False, max_workers=4),
        ]
    )

    print(">>> Optimizando hardware: El coche usa hilos y procesos según la tarea.")
    pipe.run({})
