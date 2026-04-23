from typing import Any, Dict
"""
DEMO LEVEL 56: Sistema de Eventos (Event Dispatcher)
---------------------------------------------
Adds: Sistema de eventos para notificaciones en tiempo real.
Continues: Checkpoints de L29.

DIAGRAM:
(leer_sensores)
      |
      v
[event: sensor_error] --> [listener: notificar_error]
[event: low_battery]  --> [listener: alert_driver]
"""

from wpipe import Pipeline, step

@step(name="leer_sensores")
def leer_sensores(data: dict) -> None:

    """Leer sensores step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("📡 Leyendo sensores del vehículo...")
    return {"sensores": "OK", "nivel_bateria": 15}

@step(name="notificar_error")
def notificar_error(context: Any) -> None:

    """Notificar error step.

    Args:

        context: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🔔 [EVENTO] Error crítico de sensores detectado")
    return {"notificado": True}

@step(name="alert_driver")
def alert_driver(context: Any) -> None:

    """Alert driver step.

    Args:

        context: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🔔 [EVENTO] Batería baja - Alertando al conductor")
    return {"alerta_enviada": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l56_eventsystem", verbose=True)

    pipe.add_event(
        event_type="error",
        event_name="sensor_error",
        message="Sensor defectuoso detectado",
    )

    pipe.add_event(
        event_type="warning",
        event_name="low_battery",
        message="Nivel de batería bajo",
    )

    pipe.set_steps([leer_sensores])
    print("\n>>> Startsndo sistema de eventos...\n")
    pipe.run({})
