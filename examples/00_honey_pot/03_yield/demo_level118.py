"""
DEMO LEVEL 118: Múltiples Dependencias
-------------------------------------
Añade: Múltiples depends_on.
Continúa: L117.

DIAGRAMA:
step(depends_on=["a", "b"])
"""

from wpipe import Pipeline, step


@step(name="tarea_a")
def tarea_a(data):
    print("📗 Tarea A")
    return {"a": True}


@step(name="tarea_b")
def tarea_b(data):
    print("📘 Tarea B")
    return {"b": True}


@step(name="tarea_c", depends_on=["tarea_a", "tarea_b"])
def tarea_c(data):
    print("📙 Tarea C (dependencies: A + B)")
    return {"c": True}


if __name__ == "__main__":
    print(">>> Múltiples dependencias...")

    pipe = Pipeline(pipeline_name="Viaje_L118", verbose=True)
    pipe.set_steps([tarea_a, tarea_b, tarea_c])
    pipe.run({})
