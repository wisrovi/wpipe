"""
DEMO LEVEL 137: Background con Tuple Step
------------------------------------------
Adds: Background acepta tuplas (func, name, version).
Continues: L136.

DIAGRAM:
Background((task, "name", "v1.0"))
"""

import time

from wpipe import Pipeline, step
from wpipe.pipe.components.logic_blocks import Background


@step(name="main")
def main(data):
    print("📌 Tarea principal...")
    return {"done": True}


def tuple_task(data):
    """Tarea como tupla."""
    print("📋 [TUPLE] Ejecutando tarea con nombre personalizado...")
    time.sleep(0.1)
    return {"tuple_done": True}


@step(name="finish")
def finish(data):
    print("✅ Finalizado!")
    return data


if __name__ == "__main__":
    print(">>> DEMO 137: Background con Tuple Step")
    print("=" * 50)

    pipe = Pipeline(pipeline_name="demo_137", verbose=False)
    pipe.set_steps([
        main,
        Background((tuple_task, "Mi Tarea Personalizada", "v2.0")),
        finish,
    ])

    result = pipe.run({})
    print("\n✅ Background acepta tuplas (func, name, version)!")