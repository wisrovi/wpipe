"""
DEMO LEVEL 102: get_top_slow_steps
---------------------------------
Añade: Obtener pasos más lentos.
Continúa: L101.

DIAGRAMA:
analysis.get_top_slow_steps(limit=3)
"""

import time

from wpipe import Pipeline, step


@step(name="rapido")
def rapido(data):
    return {"ok": True}


@step(name="lento")
def lento(data):
    time.sleep(0.05)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Pasos más lentos...")

    for i in range(3):
        pipe = Pipeline(
            pipeline_name=f"Viaje_L102_{i}",
            verbose=False,
            tracking_db="output/slow102.db",
        )
        pipe.set_steps([rapido, lento])
        pipe.run({})

    slow = pipe.tracker.analysis.get_top_slow_steps(limit=3)
    print(f"\n🐢 Pasos lentos: {len(slow)}")
    for s in slow:
        print(f"  - {s.get('step_name')}: {s.get('avg_duration_ms')}ms")
