"""
DEMO LEVEL 68: Múltiples Alerts
------------------------------------
Adds: Múltiples alerts con diferentes severidades.
Continues: L67.

DIAGRAM:
(Múltiples alerts: CRITICAL, WARNING, INFO)
"""

import time

from wpipe import Pipeline, step, Metric, Severity

@step(name="validar_datos")
def validar_datos(data: dict) -> None:

    """Validar datos step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.05)
    print("✅ Datos válidos")
    return {"valido": True}

@step(name="process")
def process(data: dict) -> None:

    """Process step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    time.sleep(0.2)
    print("📊Datos procesados")
    return {"ok": True}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="viaje_l68_multiplealerts",
        verbose=True,
        tracking_db="output/multi_alerts.db",
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">100",
        severity=Severity.CRITICAL,
        steps=[
            (
                lambda d: print("🚨 [CRITICAL] Pipeline muy lento!"),
                "CriticalAlert",
                "v1.0",
            )
        ],
    )

    pipe.tracker.add_alert_threshold(
        metric=Metric.PIPELINE_DURATION,
        expression=">50",
        severity=Severity.WARNING,
        steps=[(lambda d: print("⚠️ [WARNING] Pipeline lento"), "WarnAlert", "v1.0")],
    )

    pipe.set_steps([validar_datos, process])
    print("\n>>> Probando múltiples alerts...\n")
    pipe.run({})
