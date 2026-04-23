"""
DEMO LEVEL 120: ParallelExecutor
---------------------------------
Adds: Ejecución paralela explícita.
Continues: L119.

DIAGRAM:
ParallelExecutor con steps
"""

from time import sleep

from wpipe.parallel import ParallelExecutor

def tarea_a(data):
    sleep(0.05)
    print("📗 Tarea A")
    return {"a": True}

def tarea_b(data):
    sleep(0.05)
    print("📘 Tarea B")
    return {"b": True}

if __name__ == "__main__":
    print(">>> ParallelExecutor...")

    executor = ParallelExecutor(max_workers=2)
    executor.add_step("a", tarea_a)
    executor.add_step("b", tarea_b)

    executor.execute({})

    print("✅ Ejecución paralela completada")
