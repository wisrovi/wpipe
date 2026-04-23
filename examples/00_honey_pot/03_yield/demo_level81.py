"""
DEMO LEVEL 81: Export a JSON
-------------------------------
Adds: Exportar resultados a JSON.
Continues: Tracking de L49.

DIAGRAM:
Pipeline --> (export) --> resultado.json
"""

import os

from pathlib import Path

from wpipe import Pipeline, PipelineExporter, step

def start(data):
    print("🔑 Motor iniciado")
    return {"motor": "on", "km": 100}

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
        pipeline_name="viaje_l81_exportjson",
        verbose=True,
        tracking_db="output/export_test.db",
    )
    pipe.set_steps([start, finish])
    pipe.run({})

    print("\n📤 Exportando a JSON...")
    exporter = PipelineExporter("output/export_test.db")
    json_data = exporter.export_pipeline_logs(format="json")

    if json_data:
        Path("output/viaje81.json").write_text(json_data)
        print("✅ Exportado a output/viaje81.json")
    else:
        print("ℹ No hay datos para exportar")
