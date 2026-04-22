"""
DEMO LEVEL 78: Lambda con Datos Compuestos
-------------------------------------
Añade: Lambda retornando datos complejos.
Continúa: L77.

DIAGRAMA:
(lambda d: {...})
"""

from wpipe import Pipeline, step


@step(name="mostrar_estado")
def mostrar_estado(data):
    print(f"🚗 Vel: {data.get('velocidad')} km/h")
    print(f"🌡️ Temp: {data.get('temp')}°C")
    print(f"⛽ Fuel: {data.get('fuel')}%")
    return {"ok": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L78_LambdaData", verbose=True)
    pipe.set_steps(
        [
            (lambda d: {"velocidad": 120, "temp": 22, "fuel": 85}, "init", "v1.0"),
            mostrar_estado,
        ]
    )
    print("\n>>> Lambda con datos múltiples...\n")
    pipe.run({})
