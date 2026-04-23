"""
DEMO LEVEL 119: timeout + depends_on
----------------------------------
Adds: Combinar timeout con depends_on.
Continues: L118.

DIAGRAM:
@step(timeout=5, depends_on=["anterior"])
"""

import time

from wpipe import Pipeline, step

@step(name="primero")
def primero(data: dict) -> None:
    """Primero step.

    Args:
        data: Input data for the step.

    Returns:
        dict: Result of the step.
    """
    print("✅ Primero")
    return {"ok": True}

@step(name="segundo", depends_on=["primero"], timeout=2)
def segundo(data: dict) -> None:

    """Segundo step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("⏱️ Segundo (con timeout)")
    time.sleep(0.1)
    return {"ok": True}

if __name__ == "__main__":
    print(">>> Timeout + depends_on...")

    pipe = Pipeline(pipeline_name="viaje_l119", verbose=True)
    pipe.set_steps([segundo])
    pipe.run({})
