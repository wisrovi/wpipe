"""
DEMO LEVEL 27: Registro de Eficiencia (Metrics)
-----------------------------------------------
Añade: Registro de métricas numéricas en tiempo real.
Acumula: Dashboard (L26).

DIAGRAMA:
(conducir)
   |-- Metric.record("consumo") -> 6.5 L
   |-- Metric.record("velocidad") -> 120 km/h
"""

import random

from wpipe import Metric, Pipeline, step


@step(name="medir_eficiencia")
def medir_eficiencia(data):
    consumo = random.uniform(5.5, 9.0)
    velocidad = random.randint(100, 130)

    # NUEVO EN L27: Grabamos datos numéricos para analítica posterior
    Metric.record("fuel_consumption", consumo, unit="L/100km")
    Metric.record("average_speed", velocidad, unit="km/h")

    print(f"📊 Telemetría: {velocidad} km/h | {consumo:.1f} L/100km")
    return {"fuel": consumo, "speed": velocidad}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Trip_Efficiency_L27",
        tracking_db="output/coche_telemetria.db",
        verbose=True,
    )
    pipe.set_steps([medir_eficiencia])
    pipe.run({})
