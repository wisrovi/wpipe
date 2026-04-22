"""
DEMO LEVEL 94: TaskTimer Múltiples Tareas
-------------------------------------
Añade: TaskTimer para múltiples tareas.
Continúa: L93.

DIAGRAMA:
TaskTimer + pipeline iteraciones
"""

import time

from wpipe import Pipeline, step, TaskTimer


@step(name="tarea")
def tarea(data):
    time.sleep(0.02)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Múltiples tareas...")

    times = []
    for i in range(3):
        with TaskTimer(f"task_{i}", timeout_seconds=1) as timer_obj:
            pipe = Pipeline(pipeline_name=f"Viaje_L94_{i}", verbose=False)
            pipe.set_steps([tarea])
            pipe.run({})
            times.append(timer_obj.elapsed_seconds)
            print(f"  ✅ iter {i}: {timer_obj.elapsed_seconds:.3f}s")

    avg = sum(times) / len(times)
    print(f"\n⏱️ Promedio: {avg:.3f}s")
