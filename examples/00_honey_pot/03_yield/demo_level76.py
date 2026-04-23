"""
DEMO LEVEL 76: Funciones Lambda
-------------------------------
Adds: Funciones lambda como pasos inline.
Continues: For loop de L75.

DIAGRAM:
(lambda d: ...) --> paso inline
"""

from wpipe import Pipeline

def start(data):
    print("🔑 Encendiendo motor")
    return {"motor": "on"}

def iniciar_lambda(data):
    print("🔑 [LAMBDA] Motor ON")
    return {"motor": "on"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l76_lambda", verbose=True)
    pipe.set_steps(
        [
            start,
            (lambda d: print("🔑 [LAMBDA]check"), "check", "v1.0"),
            iniciar_lambda,
        ]
    )
    print("\n>>> Usando funciones lambda...\n")
    pipe.run({})
