"""
DEMO LEVEL 76: Funciones Lambda
-------------------------------
Añade: Funciones lambda como pasos inline.
Continúa: For loop de L75.

DIAGRAMA:
(lambda d: ...) --> paso inline
"""

from wpipe import Pipeline


def iniciar(data):
    print("🔑 Encendiendo motor")
    return {"motor": "on"}


def iniciar_lambda(data):
    print("🔑 [LAMBDA] Motor ON")
    return {"motor": "on"}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="Viaje_L76_Lambda", verbose=True)
    pipe.set_steps(
        [
            iniciar,
            (lambda d: print("🔑 [LAMBDA]check"), "check", "v1.0"),
            iniciar_lambda,
        ]
    )
    print("\n>>> Usando funciones lambda...\n")
    pipe.run({})
