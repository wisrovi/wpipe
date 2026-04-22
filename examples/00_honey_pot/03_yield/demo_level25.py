"""
DEMO LEVEL 25: Super-Computadora (Multi-Core Benchmark)
-------------------------------------------------------
Añade: Diferencia real entre Hilos y Procesos en Parallel.
Acumula: Paralelismo (L12 y L13).

DIAGRAMA:
Parallel(4 tareas de visión pesadas)
  |-- THREADS   -> ~1.2s (Comparten CPU)
  |-- PROCESSES -> ~0.3s (Usa todos los núcleos)
"""

import time

from wpipe import Parallel, Pipeline, step


@step(name="vision_profunda")
def vision_profunda(d):
    # Carga de CPU real (matemáticas intensas)
    start = time.time()
    while time.time() - start < 0.3:
        _ = 100 * 100
    return {"ia": "done"}


if __name__ == "__main__":
    # 1. Modo Hilos
    p1 = Pipeline(pipeline_name="Modo_ECO_Hilos")
    p1.set_steps(
        [Parallel(steps=[vision_profunda] * 4, max_workers=4, use_processes=False)]
    )

    print(">>> [TEST 1] Procesando con HILOS (Compartiendo recursos)...")
    t1 = time.time()
    p1.run({})
    print(f"⏱️ Tiempo Hilos: {time.time() - t1:.2f}s\n")

    # 2. Modo Procesos (NUEVO L25)
    # como nota, al usar el use_processes=True, se debe tener en cuenta que los datos de la bodega deben ser serializables para poderl pasarlos entre procesos
    p2 = Pipeline(pipeline_name="Modo_SPORT_Procesos")
    p2.set_steps(
        [Parallel(steps=[vision_profunda] * 4, max_workers=4, use_processes=True)]
    )

    print(">>> [TEST 2] Procesando con PROCESOS (Potencia Total)...")
    t2 = time.time()
    p2.run({})
    print(f"⏱️ Tiempo Procesos: {time.time() - t2:.2f}s")
