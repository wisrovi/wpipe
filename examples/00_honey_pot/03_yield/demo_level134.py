"""
DEMO LEVEL 134: Background con Pipeline Anidado
-----------------------------------------------
Adds: Background ejecutando un pipeline anidado.
Continues: L133.

DIAGRAM:
Pipeline → Background(sub_pipeline) → main_continues
"""

import time

from wpipe import Pipeline, step
from wpipe.pipe.components.logic_blocks import Background


@step(name="prepare")
def prepare(data):
    """Preparación."""
    print("📌 Preparando...")
    return {"prepared": True}


@step(name="nested_step_1")
def nested_step_1(data):
    """Paso anidado 1."""
    print("  📦 [Nested] Procesando paso 1...")
    return {"nested_1": True}


@step(name="nested_step_2")
def nested_step_2(data):
    """Paso anidado 2."""
    print("  📦 [Nested] Procesando paso 2...")
    time.sleep(0.1)
    return {"nested_2": True}


@step(name="continue_main")
def continue_main(data):
    """Continúa en pipeline principal."""
    print("✅ Pipeline principal continúa sin esperar el nested!")
    return data


if __name__ == "__main__":
    print(">>> DEMO 134: Background con Pipeline Anidado")
    print("=" * 50)

    sub_pipeline = Pipeline(pipeline_name="sub_pipeline", verbose=False)
    sub_pipeline.set_steps([nested_step_1, nested_step_2])

    pipe = Pipeline(pipeline_name="demo_134", verbose=False)
    pipe.set_steps([
        prepare,
        Background(sub_pipeline),
        continue_main,
    ])

    result = pipe.run({})
    print("\n✅ Pipeline principal NO esperó el sub-pipeline!")