"""
DEMO LEVEL 115: AutoRegister Completo
---------------------------------
Añade: Registro completo con todas las opciones.
Continúa: L114.

DIAGRAMA:
AutoRegister con timeout + depends_on
"""

from wpipe import Pipeline, step, AutoRegister


@step(name="iniciar", tags=["inic"])
def iniciar(data):
    print("🔑 Iniciar")
    return {"ok": True}


@step(name="procesar", depends_on=["iniciar"], timeout=5, tags=["proc"])
def procesar(data):
    print("⚡ Procesar")
    return {"ok": True}


if __name__ == "__main__":
    print(">>> AutoRegister completo...")

    pipe = Pipeline(pipeline_name="Viaje_L115", verbose=True)
    AutoRegister.register_all(pipe)

    pipe.set_steps([iniciar, procesar])
    pipe.run({})
