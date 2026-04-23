"""
DEMO LEVEL 74: For con Condition
------------------------------------
Adds: Condition dentro de For loop.
Continues: L73.

DIAGRAM:
For() {
    Condition(obstaculo) {
        branch_true: freno
        branch_false: acelerar
    }
}
"""

import random

from wpipe import Pipeline, For, Condition, step

@step(name="evaluar_situacion")
def evaluar_situacion(data: dict) -> None:

    """Evaluar situacion step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    obstaculo = random.random() < 0.3
    return {"obstaculo": obstaculo}

@step(name="frenar")
def frenar(data: dict) -> None:

    """Frenar step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🛑 FRENANDO")
    return {"action": "brake"}

@step(name="acelerar")
def acelerar(data: dict) -> None:

    """Acelerar step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🚀 ACELERANDO")
    return {"action": "accelerate"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="viaje_l74_forcondition", verbose=True)
    pipe.set_steps(
        [
            For(
                iterations=3,
                steps=[
                    evaluar_situacion,
                    Condition(
                        expression="obstaculo == True",
                        branch_true=[frenar],
                        branch_false=[acelerar],
                    ),
                ],
            )
        ]
    )
    print("\n>>> Evaluación en bucle...\n")
    pipe.run({})
