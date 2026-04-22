"""
DEMO LEVEL 100: Alerts Historial
--------------------------------
Añade: Ver historial completo de alerts.
Continúa: L99.

DIAGRAMA:
get_fired_alerts() en pipeline diferente
"""

import time

from wpipe import Pipeline, step, Metric, Severity


@step(name="tarea")
def tarea(data):
    time.sleep(0.02)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Historial de alerts...")

    pipe = Pipeline(
        pipeline_name="Viaje_L100_History",
        verbose=True,
        tracking_db="output/alerts100.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">1",
        severity=Severity.WARNING,
    )

    pipe.set_steps([tarea])
    pipe.run({})

    print(">>> Corriendo segundo pipeline...")
    pipe2 = Pipeline(
        pipeline_name="Viaje_L100b",
        verbose=False,
        tracking_db="output/alerts100.db",
    )
    pipe2.set_steps([tarea])
    pipe2.run({})

    alerts = pipe.tracker.get_fired_alerts()
    print(f"\n🚨 Total en historial: {len(alerts)}")
