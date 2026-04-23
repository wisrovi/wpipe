"""
DEMO LEVEL 66: Alert Threshold (Pipeline Lento)
-----------------------------------------------
Adds: Alerta cuando pipeline excede tiempo.
Continues: Métricas de L48.

DIAGRAM:
[tracker.add_alert_threshold(metric=DURATION, >50ms)]
      |
      v
(paso_lento) --> Alerta si > 50ms
"""

import time

from wpipe import Pipeline, step, Metric, Severity

@step(name="proceso_lento")
def proceso_lento(data: dict) -> None:

    """Proceso lento step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.1)
    print("⏳ Proceso completado (tardó 100ms)")
    return {"listo": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l66_alertthreshold",
        verbose=True,
        tracking_db="output/alert_test.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">50",
        severity=Severity.WARNING,
        steps=[
            (lambda d: print("⚠️ [ALERTA] Pipeline lento detectado"), "Alert", "v1.0")
        ],
    )

    pipe.set_steps([proceso_lento])
    print("\n>>> Probando alert threshold...\n")
    pipe.run({})
