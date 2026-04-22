"""
DEMO LEVEL 82: Export a CSV
-------------------------------
Añade: Exportar resultados a CSV.
Continúa: L81.

DIAGRAMA:
Pipeline --> (export) --> resultado.csv
"""

import os

from pathlib import Path

from wpipe import Pipeline, PipelineExporter, step


def iniciar(data):
    print("🔑 Motor iniciado")
    return {"motor": "on"}


@step(name="finalizar")
def finalizar(data):
    print("🏁 Viaje completado")
    return {"destino": "llegado"}


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="Viaje_L82_ExportCSV",
        verbose=True,
        tracking_db="output/export_csv.db",
    )
    pipe.set_steps([iniciar, finalizar])
    pipe.run({})

    print("\n📤 Exportando a CSV...")
    exporter = PipelineExporter("output/export_csv.db")
    csv_data = exporter.export_pipeline_logs(format="csv")

    if csv_data:
        Path("output/viaje82.csv").write_text(csv_data)
        print("✅ Exportado a output/viaje82.csv")
    else:
        print("ℹ No hay datos para exportar")
