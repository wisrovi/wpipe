from typing import Any, Dict
"""
DEMO LEVEL 57: Checkpoints con Callbacks
---------------------------------------
Adds: Checkpoints que disparan callbacks al cumplir condición.
Continues: Eventos de L56.

DIAGRAM:
[Checkpoint: fuel < 20] --True--> [mostrar_alerta_combustible]
[Checkpoint: temp > 90]  --False--> (no se dispara)

"""

from wpipe import Pipeline, step

@step(name="start_engine")
def start_engine(data: dict) -> None:

    """Start engine step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🚀 Motor arrancado")
    return {"fuel": 15, "temp": 85}

@step(name="monitor_engine")
def monitor_engine(data: dict) -> None:

    """Monitor engine step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("📊 Monitoreando motor...")
    return data

@step(name="mostrar_alerta_combustible")
def mostrar_alerta_combustible(context: Any) -> None:

    """Mostrar alert combustible step.

    Args:

        context: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("⛽ [CHECKPOINT] ¡Alerta de combustible!")
    return {"alert": "combustible"}

@step(name="mostrar_alerta_temperatura")
def mostrar_alerta_temperatura(context: Any) -> None:

    """Mostrar alert temperatura step.

    Args:

        context: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🌡️ [CHECKPOINT] ¡Alerta de temperatura!")
    return {"alert": "temperatura"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l57_checkpoints", verbose=True)

    pipe.add_checkpoint(
        checkpoint_name="fuel_low",
        expression="fuel < 20",
        steps=[mostrar_alerta_combustible],
    )

    pipe.add_checkpoint(
        checkpoint_name="temp_high",
        expression="temp > 90",
        steps=[mostrar_alerta_temperatura],
    )

    pipe.set_steps([start_engine, monitor_engine])
    print("\n>>> Startsndo con checkpoints...\n")
    pipe.run({})
