from typing import Any, Dict
"""
DEMO LEVEL 60: Eventos con Acciones Automáticas
---------------------------------------
Adds: Eventos que disparan acciones automáticamente.
Continues: Sistema de eventos de L56.

DIAGRAM:
[event: system_shutdown] --> [steps: apagar_sistemas, guardar_estado]
"""

from wpipe import Pipeline, step

@step(name="iniciar_sistema")
def iniciar_sistema(data: dict) -> None:

    """Startsr sistema step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🟢 Sistema iniciado")
    return {"estado": "iniciado"}

@step(name="apagar_sistemas")
def apagar_sistemas(context: Any) -> None:

    """Apagar sistemas step.

    Args:

        context: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🔴 Apagando sistemas...")
    return {"sistemas": "apagados"}

@step(name="guardar_estado")
def guardar_estado(context: Any) -> None:

    """Guardar estado step.

    Args:

        context: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("💾 Guardando estado en memoria...")
    return {"estado": "guardado"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l60_eventactions", verbose=True)

    pipe.add_event(
        event_type="shutdown",
        event_name="system_shutdown",
        message="Sistema cerrándose",
        steps=[apagar_sistemas, guardar_estado],
    )

    pipe.set_steps([iniciar_sistema])
    print("\n>>> Startsndo con eventos que disparan acciones...\n")
    pipe.run({})
