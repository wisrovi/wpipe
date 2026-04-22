"""
DEMO LEVEL 57: Checkpoints con Callbacks
---------------------------------------
Añade: Checkpoints que disparan callbacks al cumplir condición.
Continúa: Eventos de L56.

DIAGRAMA:
[Checkpoint: fuel < 20] --True--> [mostrar_alerta_combustible]
[Checkpoint: temp > 90]  --False--> (no se dispara)

"""

from wpipe import Pipeline, step


@step(name="start_engine")
def start_engine(data):
    print("🚀 Motor arrancado")
    return {"fuel": 15, "temp": 85}


@step(name="monitor_engine")
def monitor_engine(data):
    print("📊 Monitoreando motor...")
    return data


@step(name="mostrar_alerta_combustible")
def mostrar_alerta_combustible(context):
    print("⛽ [CHECKPOINT] ¡Alerta de combustible!")
    return {"alerta": "combustible"}


@step(name="mostrar_alerta_temperatura")
def mostrar_alerta_temperatura(context):
    print("🌡️ [CHECKPOINT] ¡Alerta de temperatura!")
    return {"alerta": "temperatura"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L57_Checkpoints", verbose=True)

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
    print("\n>>> Iniciando con checkpoints...\n")
    pipe.run({})
