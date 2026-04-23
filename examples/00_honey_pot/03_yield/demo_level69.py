"""
DEMO LEVEL 69: Alerts con Condición
-----------------------------------
Adds: Alerts evaluados con expresiones.
Continues: L68.

DIAGRAM:
(Alert: metric < valor)
"""

import time

from wpipe import Pipeline, step, Metric, Severity

@step(name="tarea_rapida")
def tarea_rapida(data: dict) -> None:

    """Tarea rapida step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.02)
    print("⚡ Tarea rápida")
    return {"tiempo": 20}

@step(name="tarea_normal")
def tarea_normal(data: dict) -> None:

    """Tarea normal step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.05)
    print("📊 Tarea normal")
    return {"tiempo": 50}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l69_conditionalalert",
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
