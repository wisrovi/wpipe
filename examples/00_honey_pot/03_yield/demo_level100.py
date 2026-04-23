"""
DEMO LEVEL 100: Alerts Historial
--------------------------------
Adds: View history completo de alerts.
Continues: L99.

DIAGRAM:
get_fired_alerts() en pipeline diferente
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
    print(">>> Alerts history...")

    pipe = Pipeline(
        pipeline_name="viaje_l100_history",
        verbose=True,
        tracking_db="output/alerts100.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">1",
        severity=Severity.WARNING,
    )

    pipe.set_steps([task])
    pipe.run({})

    print(">>> Running second pipeline...")
    pipe2 = Pipeline(
        pipeline_name="viaje_l100b",
        verbose=False,
        tracking_db="output/alerts100.db",
    )
    pipe2.set_steps([task])
    pipe2.run({})

    alerts = pipe.tracker.get_fired_alerts()
    print(f"\n🚨 Total in history: {len(alerts)}")
