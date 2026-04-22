"""
DEMO LEVEL 99: Múltiples Alerts
-------------------------------
Añade: Obtener múltiples alerts.
Continúa: L98.

DIAGRAMA:
múltiples threshold --> múltiples alerts
"""

import time

from wpipe import Pipeline, step, Metric, Severity


@step(name="tarea1")
def tarea1(data):
    time.sleep(0.02)
    return {"ok": True}


@step(name="tarea2")
def tarea2(data):
    time.sleep(0.1)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Múltiples alerts...")

    pipe = Pipeline(
        pipeline_name="Viaje_L99_MultiAlerts",
        verbose=True,
        tracking_db="output/alerts99.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">10",
        severity=Severity.WARNING,
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">100",
        severity=Severity.CRITICAL,
    )

    pipe.set_steps([tarea1, tarea2])
    pipe.run({})

    alerts = pipe.tracker.get_fired_alerts()
    print(f"\n🚨 Total alerts: {len(alerts)}")
    for a in alerts:
        print(f"  - {a.get('severity')}: {a.get('metric_value')}ms")
