"""
DEMO LEVEL 92: TaskTimer con Timeout
-----------------------------------
Adds: Verificar si se exceede el timeout.
Continues: L91.

DIAGRAM:
TaskTimer(timeout=0.05s) -> exceede si > 0.05s
"""

import time

from wpipe import Pipeline, step, TaskTimer

@step(name="tarea_lenta")
def tarea_lenta(data: dict) -> None:

    """Tarea lenta step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🐢 Tarea lenta...")
    time.sleep(0.1)
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Verificando timeout...")

    with TaskTimer("tarea92", timeout_seconds=0.05) as timer:
        pipe = Pipeline(pipeline_name="viaje_l92", verbose=True)
        pipe.set_steps([tarea_lenta])
        pipe.run({})

    print(f"\n⏱️ Tiempo: {timer.elapsed_seconds:.3f}s")
    print(f"⏱️ Excedido: {timer.exceeded_timeout()}")
