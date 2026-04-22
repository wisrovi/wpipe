"""
DEMO LEVEL 98: Filtrar Alerts por Severidad
-----------------------------------------
Añade: Filtrar alerts por severity.
Continúa: L97.

DIAGRAMA:
get_fired_alerts(severity=CRITICAL)
"""

import time

from wpipe import Pipeline, step, Metric, Severity


@step(name="tarea")
def tarea(data):
    time.sleep(0.02)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Filtrar alerts por severity...")

    pipe = Pipeline(
        pipeline_name="Viaje_L98_AlertsSeverity",
        verbose=True,
        tracking_db="output/alerts98.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">1",
        severity=Severity.CRITICAL,
    )

    pipe.set_steps([tarea])
    pipe.run({})

    alerts = pipe.tracker.get_fired_alerts()
    critical = [a for a in alerts if a.get("severity") == "critical"]
    print(f"\n🚨 Total: {len(alerts)}, Critical: {len(critical)}")
