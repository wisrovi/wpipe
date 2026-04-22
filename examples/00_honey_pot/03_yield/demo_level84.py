"""
DEMO LEVEL 84: Export Multiple Formats
------------------------------------
Añade: Exportar a múltiples formatos.
Continúa: L83.

DIAGRAMA:
Pipeline --> JSON + CSV + STATS
"""

import os

from pathlib import Path

from wpipe import Pipeline, PipelineExporter, step


@step(name="iniciar")
def iniciar(data):
    print("🔑 Motor iniciado")
    return {"motor": "on"}


@step(name="procesar")
def procesar(data):
    print("📊 Procesando...")
    return {"procesado": True}


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    db = "output/export_multi.db"
    pipe = Pipeline(pipeline_name="Viaje_L84_ExportMulti", verbose=True, tracking_db=db)
    pipe.set_steps([iniciar, procesar])
    pipe.run({})

    print("\n📤 Exportando en múltiples formatos...")
    exporter = PipelineExporter(db)

    json_data = exporter.export_pipeline_logs(format="json")
    if json_data:
        Path("output/viaje84.json").write_text(json_data)
        print("✅ JSON exportado")

    csv_data = exporter.export_pipeline_logs(format="csv")
    if csv_data:
        Path("output/viaje84.csv").write_text(csv_data)
        print("✅ CSV exportado")

    stats = exporter.export_statistics(format="json")
    if stats:
        Path("output/viaje84_stats.json").write_text(stats)
        print("✅ Statistics exportado")
