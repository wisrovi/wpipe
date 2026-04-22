"""
DEMO LEVEL 119: timeout + depends_on
----------------------------------
Añade: Combinar timeout con depends_on.
Continúa: L118.

DIAGRAMA:
@step(timeout=5, depends_on=["anterior"])
"""

import time

from wpipe import Pipeline, step


@step(name="primero")
def primero(data):
    print("✅ Primero")
    return {"ok": True}


@step(name="segundo", depends_on=["primero"], timeout=2)
def segundo(data):
    print("⏱️ Segundo (con timeout)")
    time.sleep(0.1)
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Timeout + depends_on...")

    pipe = Pipeline(pipeline_name="Viaje_L119", verbose=True)
    pipe.set_steps([segundo])
    pipe.run({})
