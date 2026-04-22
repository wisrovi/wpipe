"""
DEMO LEVEL 116: timeout decorador
---------------------------------
Añade: timeout en @step.
Continúa: Autoregister de L115.

DIAGRAMA:
@step(timeout=1)
"""

import time

from wpipe import Pipeline, step


@step(name="tarea", timeout=2)
def tarea(data):
    print("⚡ Ejecutando tarea...")
    time.sleep(0.1)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> timeout decorador...")

    pipe = Pipeline(pipeline_name="Viaje_L116", verbose=True)
    pipe.set_steps([tarea])
    pipe.run({})
