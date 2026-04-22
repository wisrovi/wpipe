"""
DEMO LEVEL 91: TaskTimer
-----------------------
Añade: Control de tiempo de ejecución.
Continúa: Monitor de L90.

DIAGRAMA:
with TaskTimer(timeout=1s)
"""

import time

from wpipe import Pipeline, step, TaskTimer


@step(name="tarea")
def tarea(data):
    print("⚡ Ejecutando tarea...")
    time.sleep(0.05)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> TaskTimer básico...")

    with TaskTimer("tarea91", timeout_seconds=1) as timer:
        pipe = Pipeline(pipeline_name="Viaje_L91", verbose=True)
        pipe.set_steps([tarea])
        pipe.run({})

    print(f"\n⏱️ Tiempo: {timer.elapsed_seconds:.3f}s")
    print(f"⏱️ Excedido: {timer.exceeded_timeout()}")
