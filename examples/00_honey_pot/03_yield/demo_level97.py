"""
DEMO LEVEL 97: get_fired_alerts con Límite
-----------------------------------------
Adds: Limitar número de alerts devueltos.
Continues: L96.

DIAGRAM:
get_fired_alerts(limit=5)
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
    time.sleep(0.02)
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Alerts con límite...")

    pipe = Pipeline(
        pipeline_name="viaje_l97_getalertslimit",
        verbose=True,
        tracking_db="output/alerts97.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">1",
        severity=Severity.WARNING,
    )

    pipe.set_steps([task])
    pipe.run({})

    alerts = pipe.tracker.get_fired_alerts(limit=5)
    print(f"\n🚨 Alerts: {len(alerts)}")
