"""
DEMO LEVEL 17: Monitor del Motor de IA (Recursos)
-------------------------------------------------
Añade: collect_system_metrics=True para vigilar la carga del coche.
Acumula: Inferencia pesada (L13).

DIAGRAMA:
[Inicio Monitor] ------------------+
      |                            | (Vigila CPU/RAM en segundo plano)
      v                            |
(Procesar Redes Neuronales) <------+
      |
      v
[Log de Recursos] -> Reporta picos de consumo del sistema ADAS.
"""

import time

from wpipe import Parallel, Pipeline, step


@step(name="ia_vision_360")
def ia_vision_360(data):
    print("🧠 Procesando visión artificial 360°...")
    time.sleep(0.5)  # Simula procesamiento intensivo
    return {"detecciones": "OK"}


if __name__ == "__main__":
    # Activamos la monitorización de recursos del sistema
    pipe = Pipeline(
        pipeline_name="Viaje_L17_Performance",
        verbose=True,
        collect_system_metrics=True,  # <--- NUEVO: Monitoriza el hardware
    )

    pipe.set_steps([Parallel(steps=[ia_vision_360] * 4, max_workers=4)])

    print(">>> Iniciando viaje. Observa los logs de métricas al finalizar...")
    pipe.run({})
