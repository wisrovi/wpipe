"""
DEMO LEVEL 104: Pipeline Analytics
------------------------------
Adds: Análisis completo de pipelines.
Continues: L103.

DIAGRAM:
analysis.get_pipelines_analysis()
"""

from wpipe import Pipeline, step

@step(name="start")
def start(data: dict) -> None:

    """Start step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    return {"motor": "on"}

@step(name="process")
def process(data: dict) -> None:

    """Process step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Análisis de pipelines...")

    pipe = Pipeline(
        pipeline_name="viaje_l104_pipelines",
        verbose=True,
        tracking_db="output/pipelines104.db",
    )
    pipe.set_steps([start, process])
    pipe.run({})

    analysis = pipe.tracker.analysis.get_pipelines_analysis()
    print(f"\n📊 Análisis:")
    print(f"  Total: {len(analysis)}")
