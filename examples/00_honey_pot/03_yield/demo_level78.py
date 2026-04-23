"""
DEMO LEVEL 78: Lambda con Datos Compuestos
-------------------------------------
Adds: Lambda retornando datos complejos.
Continues: L77.

DIAGRAM:
(lambda d: {...})
"""

from wpipe import Pipeline, step

@step(name="mostrar_estado")
def mostrar_estado(data: dict) -> None:

    """Mostrar estado step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print(f"🚗 Vel: {data.get('speed')} km/h")
    print(f"🌡️ Temp: {data.get('temp')}°C")
    print(f"⛽ Fuel: {data.get('fuel')}%")
    return {"ok": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l78_lambdadata", verbose=True)
    pipe.set_steps(
        [
            (lambda d: {"speed": 120, "temp": 22, "fuel": 85}, "init", "v1.0"),
            mostrar_estado,
        ]
    )
    print("\n>>> Lambda con datos múltiples...\n")
    pipe.run({})
