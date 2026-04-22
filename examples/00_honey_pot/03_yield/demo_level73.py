"""
DEMO LEVEL 73: For Anidado
-------------------------------------
Añade: For loops anidados.
Continúa: L72.

DIAGRAMA:
For(iterations=2) {
    For(iterations=2) {
        procesar()
    }
}
"""

from wpipe import Pipeline, For, step


@step(name="procesar_tramo")
def procesar_tramo(data):
    outer = data.get("_loop_iteration", 0)
    print(f"🛣️ Tramo: {outer}")
    return {"tramo": outer}


@step(name="procesar_segmento")
def procesar_segmento(data):
    inner = data.get("_loop_iteration", 0)
    print(f"  📍 Segmento: {inner}")
    return {"segmento": inner}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L73_NestedFor", verbose=True)
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
