"""
DEMO LEVEL 95: TaskTimer + Alerta
---------------------------------
Añade: Alertar cuando se exceede timeout.
Continúa: L94.

DIAGRAMA:
TaskTimer(timeout) + exceeded --> alert
"""

import time

from wpipe import Pipeline, step, TaskTimer


@step(name="tarea")
def tarea(data):
    print("⚡ Ejecutando...")
    return {"ok": True}


if __name__ == "__main__":
    print(">>> TaskTimer con alerta...")

    timeout = 0.05
    with TaskTimer("tarea95", timeout_seconds=timeout) as timer:
        time.sleep(0.02)
        pipe = Pipeline(pipeline_name="Viaje_L95", verbose=True)
        pipe.set_steps([tarea])
        pipe.run({})

    exceeded = timer.exceeded_timeout()
    print(f"\n⏱️ Timeout: {timeout}s")
    print(f"⏱️ Excedido: {exceeded}")

    if exceeded:
        print("⚠️ ALERTA: Tiempo excedido!")
