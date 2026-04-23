"""
DEMO LEVEL 112: AutoRegister por Tag
---------------------------------
Adds: Registro filtrado por tags.
Continues: L111.

DIAGRAM:
register_by_tag(pipeline, "inic")
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
    print(">>> Registro por tag...")

    pipe = Pipeline(pipeline_name="viaje_l112", verbose=True)
    AutoRegister.register_by_tag(pipe, "inic")

    pipe.set_steps([start, verificar])
    pipe.run({})
