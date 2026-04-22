"""
DEMO LEVEL 66: Alert Threshold (Pipeline Lento)
-----------------------------------------------
Añade: Alerta cuando pipeline excede tiempo.
Continúa: Métricas de L48.

DIAGRAMA:
[tracker.add_alert_threshold(metric=DURATION, >50ms)]
      |
      v
(paso_lento) --> Alerta si > 50ms
"""

import time

from wpipe import Pipeline, step, Metric, Severity


@step(name="proceso_lento")
def proceso_lento(data):
    time.sleep(0.1)
    print("⏳ Proceso completado (tardó 100ms)")
    return {"listo": True}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Viaje_L66_AlertThreshold",
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
