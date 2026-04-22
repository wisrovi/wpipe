"""
DEMO LEVEL 72: For con Condición de Parada
-----------------------------------------
Añade: For con validation_expression para detener.
Continúa: L71.

DIAGRAMA:
For(validation_expression="_loop_iteration < 3") {
    conducir()
}
"""

from wpipe import Pipeline, For, step


@step(name="conducir")
def conducir(data):
    iteration = data.get("_loop_iteration", 0)
    print(f"🚗 Conduciendo iteración: {iteration}")
    return {"distancia": iteration * 10}


@step(name="verificar_llegada")
def verificar_llegada(data):
    distancia = data.get("distancia", 0)
    print(f"🏁 Destino: {distancia}km")
    return {"verificado": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L72_WhileFuel", verbose=True)
    pipe.set_steps(
        [
            For(
                iterations=10,
                validation_expression="_loop_iteration < 3",
                steps=[conducir],
            ),
            verificar_llegada,
        ]
    )
    print("\n>>> Conducción con parada automática...\n")
    pipe.run({})
