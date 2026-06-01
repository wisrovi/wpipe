"""
DEMO LEVEL 139: Background sin capture_error (default)
-------------------------------------------------------
Adds: Background con capture_error=False por defecto.
Continues: L138.

DIAGRAM:
Background(task) = Background(task, capture_error=False)
"""

import time

from wpipe import Pipeline, step
from wpipe.pipe.components.logic_blocks import Background


@step(name="start")
def start(data):
    print("📌 Iniciando...")
    return {"started": True}


@step(name="failing_task")
def failing_task(data):
    print("🔄 [BACKGROUND] Tarea que fallará (sin capture)...")
    time.sleep(0.05)
    raise RuntimeError("Error silencioso")


@step(name="continue_step")
def continue_step(data):
    print("✅ Pipeline continúa (error ignorado)...")
    return data


if __name__ == "__main__":
    print(">>> DEMO 139: Background sin capture_error")
    print("=" * 50)

    pipe = Pipeline(pipeline_name="demo_139", verbose=True)

    pipe.set_steps([
        start,
        Background(failing_task),  # capture_error=False por defecto
        continue_step,
    ])

    result = pipe.run({})
    print("\n✅ El error fue ignorado (silent fail)!")