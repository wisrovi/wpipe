"""
DEMO LEVEL 70: Alert por Step Específico
------------------------------------
Adds: Alert solo para steps específicos.
Continues: L69.

DIAGRAM:
(Alert: step='tarea_lenta')
"""

import time

from wpipe import Pipeline, step, Metric, Severity

@step(name="tarea_normal")
def tarea_normal(data: dict) -> None:

    """Tarea normal step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.02)
    print("✅ Normal")
    return {"ok": True}

@step(name="tarea_lenta")
def tarea_lenta(data: dict) -> None:

    """Tarea lenta step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.15)
    print("🐢 Lenta (150ms)")
    return {"ok": True}

@step(name="otra_normal")
def otra_normal(data: dict) -> None:

    """Otra normal step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("✅ Otra normal")
    return {"ok": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l70_specificalert",
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
