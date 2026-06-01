"""
DEMO LEVEL 131: Background Task Básico
-------------------------------------
Adds: Background task sin bloquear el pipeline.
Continues: L130.

DIAGRAM:
Pipeline → [Background] → next_step
"""

import time

from wpipe import Pipeline, step
from wpipe.pipe.components.logic_blocks import Background


@step(name="main_task")
def main_task(data):
    """Tarea principal."""
    print("📌 Ejecutando tarea principal...")
    time.sleep(0.05)
    return {"main_done": True}


@step(name="background_task")
def background_task(data):
    """Tarea en background."""
    print("🔄 [BACKGROUND] Iniciando tarea en segundo plano...")
    time.sleep(0.2)
    print("🔄 [BACKGROUND] ¡Tarea completada!")
    return {"bg_done": True}


@step(name="next_step")
def next_step(data):
    """Siguiente paso después de background."""
    print("✅ Continuando con el siguiente paso...")
    return data


if __name__ == "__main__":
    print(">>> DEMO 131: Background Task Básico")
    print("=" * 50)

    start = time.time()

    pipe = Pipeline(pipeline_name="demo_131", verbose=False)
    pipe.set_steps([
        main_task,
        Background(background_task),
        next_step,
    ])

    result = pipe.run({})

    elapsed = time.time() - start
    print(f"\n⏱️ Tiempo total: {elapsed*1000:.0f}ms")
    print("✅ El pipeline NO esperó 200ms del background!")