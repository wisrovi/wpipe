"""
DEMO LEVEL 83: Export Statistics
---------------------------------
Añade: Exportar estadísticas.
Continúa: L82.

DIAGRAMA:
Pipeline --> (export_statistics) --> stats.json
"""

import os

from pathlib import Path

from wpipe import Pipeline, PipelineExporter, step


@step(name="iniciar")
def iniciar(data):
    return {"motor": "on"}


@step(name="procesar")
def procesar(data):
    return {"procesado": True}


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="Viaje_L83_ExportStats",
        verbose=True,
        tracking_db="output/export_stats.db",
    )
    pipe.set_steps([iniciar, procesar])
    pipe.run({})

    print("\n📊 Exportando estadísticas...")
    exporter = PipelineExporter("output/export_stats.db")
    stats = exporter.export_statistics(format="json")

    if stats:
        Path("output/viaje83_stats.json").write_text(stats)
        print("✅ Exportado a output/viaje83_stats.json")
    else:
        print("ℹ No hay estadísticas")
