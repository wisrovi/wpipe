"""
DEMO LEVEL 111: AutoRegister
------------------------------
Adds: Registro automático de steps.
Continues: Wsqlite de L110.

DIAGRAM:
@step + AutoRegister.register_all()
"""

from wpipe import Pipeline, step, AutoRegister

@step(name="start", tags=["inic"])
def start(data: dict) -> None:

    """Start step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🔑 Startsndo...")
    return {"estado": "iniciado"}

@step(name="process", tags=["proc"])
def process(data: dict) -> None:

    """Process step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("⚡ Procesando...")
    return {"procesado": True}

if __name__ == "__main__":
    print(">>> AutoRegister...")

    pipe = Pipeline(pipeline_name="viaje_l111", verbose=True)
    AutoRegister.register_all(pipe)

    pipe.set_steps([start, process])
    pipe.run({})
