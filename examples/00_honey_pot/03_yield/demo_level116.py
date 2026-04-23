"""
DEMO LEVEL 116: timeout decorador
---------------------------------
Adds: timeout en @step.
Continues: Autoregister de L115.

DIAGRAM:
@step(timeout=1)
"""

import time

from wpipe import Pipeline, step

@step(name="task", timeout=2)
def task(data: dict) -> None:
    """Task step.

    Args:
        data: Input data for the step.

    Returns:
        dict: Result of the step.
    """
    print("⚡ Ejecutando task...")
    time.sleep(0.1)
    return {"ok": True}

if __name__ == "__main__":
    print(">>> timeout decorador...")

    pipe = Pipeline(pipeline_name="viaje_l116", verbose=True)
    pipe.set_steps([task])
    pipe.run({})
