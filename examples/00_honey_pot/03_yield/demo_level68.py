"""
DEMO LEVEL 68: Múltiples Alerts
------------------------------------
Añade: Múltiples alerts con diferentes severidades.
Continúa: L67.

DIAGRAMA:
(Múltiples alerts: CRITICAL, WARNING, INFO)
"""

import time

from wpipe import Pipeline, step, Metric, Severity


@step(name="validar_datos")
def validar_datos(data):
    time.sleep(0.05)
    print("✅ Datos válidos")
    return {"valido": True}


@step(name="procesar")
def procesar(data):
    time.sleep(0.2)
    print("📊Datos procesados")
    return {"ok": True}


if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="Viaje_L68_MultipleAlerts",
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

    pipe.set_steps([validar_datos, procesar])
    print("\n>>> Probando múltiples alerts...\n")
    pipe.run({})
