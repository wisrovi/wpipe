"""
DEMO LEVEL 96: get_fired_alerts
-----------------------------
Adds: Obtener alerts disparados.
Continues: Alert threshold de L70.

DIAGRAM:
tracker.get_fired_alerts() --> lista de alerts
"""

import time

from wpipe import Pipeline, step, Metric, Severity

@step(name="task")
def task(data: dict) -> None:

    """Task step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.05)
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Obteniendo alerts disparados...")

    pipe = Pipeline(
        pipeline_name="viaje_l96_getalerts",
        verbose=True,
        tracking_db="output/alerts96.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">1",
        severity=Severity.CRITICAL,
    )

    pipe.set_steps([task])
    pipe.run({})

    alerts = pipe.tracker.get_fired_alerts()
    print(f"\n🚨 Alerts disparados: {len(alerts)}")
    for a in alerts:
        print(f"  - {a}")
