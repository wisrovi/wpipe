"""
DEMO LEVEL 133: Múltiples Background Tasks
-----------------------------------------
Adds: Múltiples tareas background ejecutándose en paralelo.
Continues: L132.

DIAGRAM:
Pipeline → [Background] → [Background] → [Background] → next
"""

import time
import threading

from wpipe import Pipeline, step
from wpipe.pipe.components.logic_blocks import Background


counter = {"value": 0}
lock = threading.Lock()


@step(name="start")
def start(data):
    """Inicio."""
    print("📌 Iniciando pipeline...")
    return {"started": True}


@step(name="task_1")
def task_1(data):
    """Tarea 1 en background."""
    with lock:
        counter["value"] += 1
    print(f"🔄 [BG-1] Contador: {counter['value']}")


@step(name="task_2")
def task_2(data):
    """Tarea 2 en background."""
    time.sleep(0.1)
    with lock:
        counter["value"] += 1
    print(f"🔄 [BG-2] Contador: {counter['value']}")


@step(name="task_3")
def task_3(data):
    """Tarea 3 en background."""
    time.sleep(0.05)
    with lock:
        counter["value"] += 1
    print(f"🔄 [BG-3] Contador: {counter['value']}")


@step(name="finish")
def finish(data):
    """Finaliza."""
    print(f"✅ Pipeline terminado. Contador final: {counter['value']}")
    return data


if __name__ == "__main__":
    print(">>> DEMO 133: Múltiples Background Tasks")
    print("=" * 50)

    start_time = time.time()

    pipe = Pipeline(pipeline_name="demo_133", verbose=False)
    pipe.set_steps([
        start,
        Background(task_1),
        Background(task_2),
        Background(task_3),
        finish,
    ])

    result = pipe.run({})

    elapsed = time.time() - start_time
    print(f"\n⏱️ Tiempo de pipeline: {elapsed*1000:.0f}ms")
    print("💡 Las 3 tareas background se ejectaron en paralelo!")
    print("💡 (Nota: Algunas pueden no completar antes de que el proceso termine)")