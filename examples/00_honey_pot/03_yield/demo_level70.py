"""
DEMO LEVEL 70: Alert por Step Específico
------------------------------------
Añade: Alert solo para steps específicos.
Continúa: L69.

DIAGRAMA:
(Alert: step='tarea_lenta')
"""

import time

from wpipe import Pipeline, step, Metric, Severity


@step(name="tarea_normal")
def tarea_normal(data):
    time.sleep(0.02)
    print("✅ Normal")
    return {"ok": True}


@step(name="tarea_lenta")
def tarea_lenta(data):
    time.sleep(0.15)
    print("🐢 Lenta (150ms)")
    return {"ok": True}


@step(name="otra_normal")
def otra_normal(data):
    print("✅ Otra normal")
    return {"ok": True}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Viaje_L70_SpecificAlert",
        verbose=True,
        tracking_db="output/specific_alert.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.STEP_DURATION,
        expression=">100",
        severity=Severity.WARNING,
        steps=[tarea_lenta],
    )

    pipe.set_steps([tarea_normal, tarea_lenta, otra_normal])
    print("\n>>> Probando alert para step específico...\n")
    pipe.run({})
