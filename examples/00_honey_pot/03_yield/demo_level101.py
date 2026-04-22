"""
DEMO LEVEL 101: tracker.analysis
---------------------------------
Añade: Análisis de rendimiento.
Continúa: Alerts de L100.

DIAGRAMA:
tracker.analysis.get_stats()
"""

from wpipe import Pipeline, step


@step(name="tarea")
def tarea(data):
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Análisis de pipeline...")

    pipe = Pipeline(
        pipeline_name="Viaje_L101_Analysis",
        verbose=True,
        tracking_db="output/analysis101.db",
    )
    pipe.set_steps([tarea])
    pipe.run({})

    stats = pipe.tracker.analysis.get_stats()
    print(f"\n📊 Stats:")
    print(f"  Pipelines: {stats.get('total_pipelines')}")
    print(f"  Éxito: {stats.get('success_rate')}%")
    print(f"  Duración avg: {stats.get('avg_duration_ms')}ms")
