"""
DEMO LEVEL 72: For con Condición de Parada
-----------------------------------------
Adds: For con validation_expression para detener.
Continues: L71.

DIAGRAM:
For(validation_expression="_loop_iteration < 3") {
    drive()
}
"""

from wpipe import Pipeline, For, step

@step(name="drive")
def drive(data: dict) -> None:

    """Drive step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    iteration = data.get("_loop_iteration", 0)
    print(f"🚗 Conduciendo iteración: {iteration}")
    return {"distancia": iteration * 10}

@step(name="verificar_llegada")
def verificar_llegada(data: dict) -> None:

    """Verificar llegada step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    distancia = data.get("distancia", 0)
    print(f"🏁 Destino: {distancia}km")
    return {"verificado": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l72_whilefuel", verbose=True)
    pipe.set_steps(
        [
            For(
                iterations=10,
                validation_expression="_loop_iteration < 3",
                steps=[drive],
            ),
            verificar_llegada,
        ]
    )
    print("\n>>> Conducción con parada automática...\n")
    pipe.run({})
