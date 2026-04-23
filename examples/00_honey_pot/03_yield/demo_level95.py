"""
DEMO LEVEL 95: TaskTimer + Alerta
---------------------------------
Adds: Alertar cuando se exceede timeout.
Continues: L94.

DIAGRAM:
TaskTimer(timeout) + exceeded --> alert
"""

import time

from wpipe import Pipeline, step, TaskTimer

@step(name="task")
def task(data: dict) -> None:

    """Task step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("⚡ Ejecutando...")
    return {"ok": True}

if __name__ == "__main__":
    print(">>> TaskTimer con alert...")

    timeout = 0.05
    with TaskTimer("tarea95", timeout_seconds=timeout) as timer:
        time.sleep(0.02)
        pipe = Pipeline(pipeline_name="viaje_l95", verbose=True)
        pipe.set_steps([task])
        pipe.run({})

    exceeded = timer.exceeded_timeout()
    print(f"\n⏱️ Timeout: {timeout}s")
    print(f"⏱️ Excedido: {exceeded}")

    if exceeded:
        print("⚠️ ALERTA: Tiempo excedido!")
