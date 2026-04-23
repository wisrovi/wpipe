"""
DEMO LEVEL 113: AutoRegister Múltiples Tags
-----------------------------------------
Adds: Registro con múltiples tags.
Continues: L112.

DIAGRAM:
registros con diferentes tags
"""

from wpipe import Pipeline, step, AutoRegister

@step(name="start", tags=["inic", "auto"])
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

@step(name="verificar", tags=["inic"])
def verificar(data: dict) -> None:

    """Verificar step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("✅ Verificando...")
    return {"verificado": True}

if __name__ == "__main__":
    print(">>> Múltiples tags...")

    pipe = Pipeline(pipeline_name="viaje_l113", verbose=True)
    AutoRegister.register_all(pipe)

    pipe.set_steps([start, process, verificar])
    pipe.run({})
