"""
DEMO LEVEL 69: Alerts con Condición
-----------------------------------
Añade: Alerts evaluados con expresiones.
Continúa: L68.

DIAGRAMA:
(Alert: metric < valor)
"""

import time

from wpipe import Pipeline, step, Metric, Severity


@step(name="tarea_rapida")
def tarea_rapida(data):
    time.sleep(0.02)
    print("⚡ Tarea rápida")
    return {"tiempo": 20}


@step(name="tarea_normal")
def tarea_normal(data):
    time.sleep(0.05)
    print("📊 Tarea normal")
    return {"tiempo": 50}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Viaje_L69_ConditionalAlert",
        verbose=True,
        tracking_db="output/cond_alert.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">80",
        severity=Severity.CRITICAL,
    )

    pipe.set_steps([tarea_rapida, tarea_normal])
    print("\n>>> Probando alert condicional...\n")
    pipe.run({})
