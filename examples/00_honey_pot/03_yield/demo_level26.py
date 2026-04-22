"""
DEMO LEVEL 26: La Pantalla Central (Dashboard)
---------------------------------------------
Añade: Conexión con la base de datos de tracking para visualización.
Acumula: Inferencia YOLO y Telemetría.

DIAGRAMA:
(Procesar Viaje) -> [Base de Datos SQLite]
      |
      +----------> [Dashboard Web] -> (Gráficos, Tiempos, Alertas)
"""

import os

from wpipe import Pipeline, step


@step(name="navegacion_activa")
def navegacion_activa(data):
    print("🗺️  Navegación: Guiando al destino... (Datos grabándose para el Dashboard)")
    return {"tramo": "Autopista A-6"}


if __name__ == "__main__":
    db_path = "output/coche_dashboard.db"
    os.makedirs("output", exist_ok=True)

    # NUEVO EN L26: Al definir tracking_db, habilitamos la 'Caja Negra' del coche
    pipe = Pipeline(pipeline_name="ADAS_System_L26", tracking_db=db_path, verbose=True)

    pipe.set_steps([navegacion_activa])

    print(f">>> CONSEJO: Abre una terminal y lanza 'wpipe dashboard {db_path}'")
    pipe.run({})
