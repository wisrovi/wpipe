"""
DEMO LEVEL 56: Sistema de Eventos (Event Dispatcher)
---------------------------------------------
Añade: Sistema de eventos para notificaciones en tiempo real.
Continúa: Checkpoints de L29.

DIAGRAMA:
(leer_sensores)
      |
      v
[event: sensor_error] --> [listener: notificar_error]
[event: low_battery]  --> [listener: alert_driver]
"""

from wpipe import Pipeline, step


@step(name="leer_sensores")
def leer_sensores(data):
    print("📡 Leyendo sensores del vehículo...")
    return {"sensores": "OK", "nivel_bateria": 15}


@step(name="notificar_error")
def notificar_error(context):
    print("🔔 [EVENTO] Error crítico de sensores detectado")
    return {"notificado": True}


@step(name="alert_driver")
def alert_driver(context):
    print("🔔 [EVENTO] Batería baja - Alertando al conductor")
    return {"alerta_enviada": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L56_EventSystem", verbose=True)

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
    print("\n>>> Iniciando sistema de eventos...\n")
    pipe.run({})
