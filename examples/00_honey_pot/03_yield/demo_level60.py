"""
DEMO LEVEL 60: Eventos con Acciones Automáticas
---------------------------------------
Añade: Eventos que disparan acciones automáticamente.
Continúa: Sistema de eventos de L56.

DIAGRAMA:
[event: system_shutdown] --> [steps: apagar_sistemas, guardar_estado]
"""

from wpipe import Pipeline, step


@step(name="iniciar_sistema")
def iniciar_sistema(data):
    print("🟢 Sistema iniciado")
    return {"estado": "iniciado"}


@step(name="apagar_sistemas")
def apagar_sistemas(context):
    print("🔴 Apagando sistemas...")
    return {"sistemas": "apagados"}


@step(name="guardar_estado")
def guardar_estado(context):
    print("💾 Guardando estado en memoria...")
    return {"estado": "guardado"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L60_EventActions", verbose=True)

    pipe.add_event(
        event_type="shutdown",
        event_name="system_shutdown",
        message="Sistema cerrándose",
        steps=[apagar_sistemas, guardar_estado],
    )

    pipe.set_steps([iniciar_sistema])
    print("\n>>> Iniciando con eventos que disparan acciones...\n")
    pipe.run({})
