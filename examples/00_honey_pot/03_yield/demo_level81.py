"""
DEMO LEVEL 81: Export a JSON
-------------------------------
Añade: Exportar resultados a JSON.
Continúa: Tracking de L49.

DIAGRAMA:
Pipeline --> (export) --> resultado.json
"""

import os

from pathlib import Path

from wpipe import Pipeline, PipelineExporter, step


def iniciar(data):
    print("🔑 Motor iniciado")
    return {"motor": "on", "km": 100}


@step(name="finalizar")
def finalizar(data):
    print("🏁 Viaje completado")
    return {"destino": "llegado"}


if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="Viaje_L81_ExportJSON",
        verbose=True,
        tracking_db="output/export_test.db",
    )
    pipe.set_steps([iniciar, finalizar])
    pipe.run({})

    print("\n📤 Exportando a JSON...")
    exporter = PipelineExporter("output/export_test.db")
    json_data = exporter.export_pipeline_logs(format="json")

    if json_data:
        Path("output/viaje81.json").write_text(json_data)
        print("✅ Exportado a output/viaje81.json")
    else:
        print("ℹ No hay datos para exportar")
