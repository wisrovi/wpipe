"""
DEMO LEVEL 67: Alert para Step Lento
------------------------------------
Adds: Alerta cuando un step específico es lento.
Continues: L66.

DIAGRAM:
[add_alert_threshold(STEP_DURATION, >50ms)]
      |
      v
(paso_lento) --> Alerta
"""

import time

from wpipe import Pipeline, step, Metric, Severity

@step(name="paso_rapido")
def paso_rapido(data: dict) -> None:

    """Paso rapido step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("⚡ Paso rápido")
    return {"ok": True}

@step(name=" paso_lento", version="v1.0")
def paso_lento(data: dict) -> None:

    """Paso lento step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.1)
    print("🐢 Paso lento (100ms)")
    return {"ok": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l67_stepalert",
        verbose=True,
        tracking_db="output/alert_step.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.STEP_DURATION,
        expression=">50",
        severity=Severity.WARNING,
        steps=[(lambda d: print("⚠️ [ALERTA] Step lento!"), "Alert", "v1.0")],
    )

    pipe.set_steps([paso_rapido, paso_lento])
    print("\n>>> Probando alert threshold para step...\n")
    pipe.run({})
