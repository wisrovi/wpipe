"""
DEMO LEVEL 117: step_depends
---------------------------------
Añade: Dependencias entre pasos.
Continúa: L116.

DIAGRAMA:
@step(depends_on=["anterior"])
"""

from wpipe import Pipeline, step


@step(name="primero")
def primero(data):
    print("1️⃣ Primero")
    return {"done": True}


@step(name="segundo", depends_on=["primero"])
def segundo(data):
    print("2️⃣ Segundo (depends_on primero)")
    return {"done": True}


if __name__ == "__main__":
    print(">>> step_depends...")

    pipe = Pipeline(pipeline_name="Viaje_L117", verbose=True)
    pipe.set_steps([segundo])
    pipe.run({})
