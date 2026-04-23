"""
DEMO LEVEL 117: step_depends
---------------------------------
Adds: Dependencias entre pasos.
Continues: L116.

DIAGRAM:
@step(depends_on=["anterior"])
"""

from wpipe import Pipeline, step

@step(name="primero")
def primero(data: dict) -> None:
    """Primero step.

    Args:
        data: Input data for the step.

    Returns:
        dict: Result of the step.
    """
    print("1️⃣ Primero")
    return {"done": True}

@step(name="segundo", depends_on=["primero"])
def segundo(data: dict) -> None:

    """Segundo step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("2️⃣ Segundo (depends_on primero)")
    return {"done": True}

if __name__ == "__main__":
    print(">>> step_depends...")

    pipe = Pipeline(pipeline_name="viaje_l117", verbose=True)
    pipe.set_steps([segundo])
    pipe.run({})
