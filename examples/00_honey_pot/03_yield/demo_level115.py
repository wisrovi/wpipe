"""
DEMO LEVEL 115: AutoRegister Completo
---------------------------------
Adds: Registro completo con todas las opciones.
Continues: L114.

DIAGRAM:
AutoRegister con timeout + depends_on
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
    print("🔑 Startsr")
    return {"ok": True}

@step(name="process", depends_on=["start"], timeout=5, tags=["proc"])
def process(data: dict) -> None:

    """Process step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("⚡ Procesar")
    return {"ok": True}

if __name__ == "__main__":
    print(">>> AutoRegister completo...")

    pipe = Pipeline(pipeline_name="viaje_l115", verbose=True)
    AutoRegister.register_all(pipe)

    pipe.set_steps([start, process])
    pipe.run({})
