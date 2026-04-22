"""
DEMO LEVEL 77: Lambda con Retorno
-------------------------------
Añade: Lambda que retorna datos.
Continúa: L76.

DIAGRAMA:
(lambda d: {"key": value})
"""

from wpipe import Pipeline


def procesar(data):
    print(f"📊 Velocidad: {data.get('velocidad')} km/h")
    return {"procesado": True}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L77_LambdaReturn", verbose=True)
    pipe.set_steps(
        [
            (lambda d: {"velocidad": 120}, "set_speed", "v1.0"),
            (lambda d: {"temperatura": 25}, "set_temp", "v1.0"),
            procesar,
        ]
    )
    print("\n>>> Lambda con retorno de datos...\n")
    pipe.run({})
