"""
DEMO LEVEL 71: For Iteración - Múltiples Framelos
------------------------------------------
Adds: For loop para process múltiples frames.
Continues: Condiciones de L20.

DIAGRAM:
For(iterations=3) {
    procesar_frame(i)
}
"""

from wpipe import Pipeline, For, step

@step(name="procesar_frame")
def procesar_frame(data: dict) -> None:

    """Procesar frame step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    iteration = data.get("_loop_iteration", 0)
    print(f"🖼️ Procesando frame: {iteration}")
    return {"frame": iteration}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l71_forloop", verbose=True)
    pipe.set_steps([For(iterations=3, steps=[procesar_frame])])
    print("\n>>> Procesando múltiples frames...\n")
    pipe.run({})
