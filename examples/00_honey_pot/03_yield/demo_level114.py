"""
DEMO LEVEL 114: AutoRegister con Dependencias
-----------------------------------------
Adds: AutoRegister con pasos que dependen de otros.
Continues: L113.

DIAGRAM:
@step(depends_on=["step1"])
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
    print("🔑 Paso 1: Startsr")
    return {"iniciado": True}

@step(name="validar", depends_on=["start"], tags=["proc"])
def validar(data: dict) -> None:

    """Validar step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("✅ Paso 2: Validar (depende de start)")
    return {"validado": True}

if __name__ == "__main__":
    print(">>> AutoRegister con dependencias...")

    pipe = Pipeline(pipeline_name="viaje_l114", verbose=True)
    AutoRegister.register_all(pipe)

    pipe.set_steps([start, validar])
    pipe.run({})
