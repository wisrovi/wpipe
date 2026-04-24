"""
DEMO LEVEL 138: Background con Condition
-----------------------------------------
Adds: Background dentro de una condición.
Continues: L137.

DIAGRAM:
Condition(..., branch_true=[Background(task)])
"""

import time

from wpipe import Pipeline, step, Condition
from wpipe.pipe.components.logic_blocks import Background


@step(name="check")
def check(data):
    print("🔍 Verificando condición...")
    data["condition"] = True
    return data


@step(name="bg_in_true")
def bg_in_true(data):
    print("🔄 [BACKGROUND] Ejecutando en branch true...")
    time.sleep(0.1)


@step(name="regular_in_false")
def regular_in_false(data):
    print("📌 Tarea regular en branch false...")


@step(name="after_condition")
def after_condition(data):
    print("✅ Después de la condición!")
    return data


if __name__ == "__main__":
    print(">>> DEMO 138: Background con Condition")
    print("=" * 50)

    pipe = Pipeline(pipeline_name="demo_138", verbose=False)
    pipe.set_steps([
        check,
        Condition(
            expression="condition == True",
            branch_true=[Background(bg_in_true)],
            branch_false=[regular_in_false],
        ),
        after_condition,
    ])

    result = pipe.run({})
    print("\n✅ Background funciona dentro de Condition!")