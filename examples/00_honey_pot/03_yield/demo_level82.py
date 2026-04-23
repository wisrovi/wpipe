"""
DEMO LEVEL 82: Export a CSV
-------------------------------
Adds: Exportar resultados a CSV.
Continues: L81.

DIAGRAM:
Pipeline --> (export) --> resultado.csv
"""

import os

from pathlib import Path

from wpipe import Pipeline, PipelineExporter, step

def start(data):
    print("🔑 Motor iniciado")
    return {"motor": "on"}

@step(name="finish")
def finish(data: dict) -> None:

    """Finish step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🏁 Viaje completado")
    return {"destino": "llegado"}

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="viaje_l82_exportcsv",
        verbose=True,
        tracking_db="output/export_csv.db",
    )
    pipe.set_steps([start, finish])
    pipe.run({})

    print("\n📤 Exportando a CSV...")
    exporter = PipelineExporter("output/export_csv.db")
    csv_data = exporter.export_pipeline_logs(format="csv")

    if csv_data:
        Path("output/viaje82.csv").write_text(csv_data)
        print("✅ Exportado a output/viaje82.csv")
    else:
        print("ℹ No hay datos para exportar")
