"""
DEMO LEVEL 73: For Anidado
-------------------------------------
Adds: For loops anidados.
Continues: L72.

DIAGRAM:
For(iterations=2) {
    For(iterations=2) {
        process()
    }
}
"""

from wpipe import Pipeline, For, step

@step(name="procesar_tramo")
def procesar_tramo(data: dict) -> None:

    """Procesar tramo step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    outer = data.get("_loop_iteration", 0)
    print(f"🛣️ Tramo: {outer}")
    return {"stretch": outer}

@step(name="procesar_segmento")
def procesar_segmento(data: dict) -> None:

    """Procesar segmento step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    inner = data.get("_loop_iteration", 0)
    print(f"  📍 Segmento: {inner}")
    return {"segmento": inner}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l73_nestedfor", verbose=True)
    pipe.set_steps(
        [
            For(
                iterations=2,
                steps=[procesar_tramo, For(iterations=2, steps=[procesar_segmento])],
            )
        ]
    )
    print("\n>>> For anidados...\n")
    pipe.run({})
