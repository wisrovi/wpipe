"""
DEMO LEVEL 103: get_trend_data
---------------------------------
Añade: Obtener datos de tendencia.
Continúa: L102.

DIAGRAMA:
analysis.get_trend_data(days=1)
"""

import time

from wpipe import Pipeline, step


@step(name="tarea")
def tarea(data):
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Tendencia de datos...")

    for i in range(2):
        pipe = Pipeline(
            pipeline_name=f"Viaje_103_{i}",
            verbose=False,
            tracking_db="output/trend103.db",
        )
        pipe.set_steps([tarea])
        pipe.run({})
        print(f"  ✅ run {i}")

    trends = pipe.tracker.analysis.get_trend_data(days=1)
    print(f"\n📈 Tendencia: {len(trends)}")
    if trends:
        print(f"  - Ejecuciones: {trends[0].get('count')}")
        print(f"  - Éxitos: {trends[0].get('success')}")
