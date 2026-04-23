"""
DEMO LEVEL 83: Export Statistics
---------------------------------
Adds: Exportar estadísticas.
Continues: L82.

DIAGRAM:
Pipeline --> (export_statistics) --> stats.json
"""

import os

from pathlib import Path

from wpipe import Pipeline, PipelineExporter, step

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
    return {"procesado": True}

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="viaje_l83_exportstats",
        verbose=True,
        tracking_db="output/export_stats.db",
    )
    pipe.set_steps([start, process])
    pipe.run({})

    print("\n📊 Exportando estadísticas...")
    exporter = PipelineExporter("output/export_stats.db")
    stats = exporter.export_statistics(format="json")

    if stats:
        Path("output/viaje83_stats.json").write_text(stats)
        print("✅ Exportado a output/viaje83_stats.json")
    else:
        print("ℹ No hay estadísticas")
