"""
DEMO LEVEL 91: TaskTimer
-----------------------
Adds: Control de tiempo de ejecución.
Continues: Monitor de L90.

DIAGRAM:
with TaskTimer(timeout=1s)
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
    print("⚡ Ejecutando task...")
    time.sleep(0.05)
    return {"ok": True}

if __name__ == "__main__":
    print(">>> TaskTimer básico...")

    with TaskTimer("tarea91", timeout_seconds=1) as timer:
        pipe = Pipeline(pipeline_name="viaje_l91", verbose=True)
        pipe.set_steps([task])
        pipe.run({})

    print(f"\n⏱️ Tiempo: {timer.elapsed_seconds:.3f}s")
    print(f"⏱️ Excedido: {timer.exceeded_timeout()}")
