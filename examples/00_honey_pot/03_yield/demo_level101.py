"""
DEMO LEVEL 101: tracker.analysis
---------------------------------
Adds: Análisis de rendimiento.
Continues: Alerts de L100.

DIAGRAM:
tracker.analysis.get_stats()
"""

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
    print(">>> Análisis de pipeline...")

    pipe = Pipeline(
        pipeline_name="viaje_l101_analysis",
        verbose=True,
        tracking_db="output/analysis101.db",
    )
    pipe.set_steps([task])
    pipe.run({})

    stats = pipe.tracker.analysis.get_stats()
    print(f"\n📊 Stats:")
    print(f"  Pipelines: {stats.get('total_pipelines')}")
    print(f"  Éxito: {stats.get('success_rate')}%")
    print(f"  Duración avg: {stats.get('avg_duration_ms')}ms")
