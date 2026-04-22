"""
DEMO LEVEL 97: get_fired_alerts con Límite
-----------------------------------------
Añade: Limitar número de alerts devueltos.
Continúa: L96.

DIAGRAMA:
get_fired_alerts(limit=5)
"""

import time

from wpipe import Pipeline, step, Metric, Severity


@step(name="tarea")
def tarea(data):
    time.sleep(0.02)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Alerts con límite...")

    pipe = Pipeline(
        pipeline_name="Viaje_L97_GetAlertsLimit",
        verbose=True,
        tracking_db="output/alerts97.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">1",
        severity=Severity.WARNING,
    )

    pipe.set_steps([tarea])
    pipe.run({})

    alerts = pipe.tracker.get_fired_alerts(limit=5)
    print(f"\n🚨 Alerts: {len(alerts)}")
