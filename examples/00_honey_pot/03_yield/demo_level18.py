"""
DEMO LEVEL 18: El Libro de Ruta (Exportación)
---------------------------------------------
Añade: PipelineExporter para guardar el historial en disco.
Acumula: Tracking de datos (L14).

DIAGRAMA:
(Viaje Finalizado) -> [Base de Datos de Tracking]
      |
      v
(PipelineExporter) -> [viaje_logs.csv]
"""

import os

from wpipe import Pipeline, PipelineExporter, step


@step(name="circular_tramo_a")
def circular_tramo_a(d):
    print("🚗 Circulando por Tramo A...")
    return {"tramo": "A", "duracion": 15}


if __name__ == "__main__":
    db_path = "output/viaje_historial.db"
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="Viaje_L18_Exporter", tracking_db=db_path, verbose=True
    )
    pipe.set_steps([circular_tramo_a])
    pipe.run({})

    # NUEVO EN L18: Exportamos el viaje a un formato legible por humanos
    print("\n>>> Generando reporte CSV para la compañía de seguros...")
    exporter = PipelineExporter(db_path)
    exporter.export_pipeline_logs("output/reporte_viaje.csv", format="csv")
    print("✅ Reporte guardado en output/reporte_viaje.csv")
