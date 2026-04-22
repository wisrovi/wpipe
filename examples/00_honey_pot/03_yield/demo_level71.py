"""
DEMO LEVEL 71: For Iteración - Múltiples Framelos
------------------------------------------
Añade: For loop para procesar múltiples frames.
Continúa: Condiciones de L20.

DIAGRAMA:
For(iterations=3) {
    procesar_frame(i)
}
"""

from wpipe import Pipeline, For, step


@step(name="procesar_frame")
def procesar_frame(data):
    iteration = data.get("_loop_iteration", 0)
    print(f"🖼️ Procesando frame: {iteration}")
    return {"frame": iteration}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L71_ForLoop", verbose=True)
    pipe.set_steps([For(iterations=3, steps=[procesar_frame])])
    print("\n>>> Procesando múltiples frames...\n")
    pipe.run({})
