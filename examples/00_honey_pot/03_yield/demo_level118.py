"""
DEMO LEVEL 118: Múltiples Dependencias
-------------------------------------
Adds: Múltiples depends_on.
Continues: L117.

DIAGRAM:
step(depends_on=["a", "b"])
"""

from wpipe import Pipeline, step

@step(name="tarea_a")
def tarea_a(data: dict) -> None:

    """Tarea a step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("📗 Tarea A")
    return {"a": True}

@step(name="tarea_b")
def tarea_b(data: dict) -> None:

    """Tarea b step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("📘 Tarea B")
    return {"b": True}

@step(name="tarea_c", depends_on=["tarea_a", "tarea_b"])
def tarea_c(data: dict) -> None:

    """Tarea c step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("📙 Tarea C (dependencies: A + B)")
    return {"c": True}

if __name__ == "__main__":
    print(">>> Múltiples dependencias...")

    pipe = Pipeline(pipeline_name="viaje_l118", verbose=True)
    pipe.set_steps([tarea_a, tarea_b, tarea_c])
    pipe.run({})
