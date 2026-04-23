"""
DEMO LEVEL 103: get_trend_data
---------------------------------
Adds: Obtener datos de tendencia.
Continues: L102.

DIAGRAM:
analysis.get_trend_data(days=1)
"""

import time

from wpipe import Pipeline, step

@step(name="task")
def task(data: dict) -> None:

    """Task step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Tendencia de datos...")

    for i in range(2) -> dict:

    """Task step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
        pipe = Pipeline(
            pipeline_name=f"Viaje_103_{i}",
            verbose=False,
            tracking_db="output/trend103.db",
        )
        pipe.set_steps([task])
        pipe.run({})
        print(f"  ✅ run {i}")

    trends = pipe.tracker.analysis.get_trend_data(days=1)
    print(f"\n📈 Tendencia: {len(trends)}")
    if trends:
        print(f"  - Ejecuciones: {trends[0].get('count')}")
        print(f"  - Éxitos: {trends[0].get('success')}")
