"""
DEMO LEVEL 114: AutoRegister con Dependencias
-----------------------------------------
Añade: AutoRegister con pasos que dependen de otros.
Continúa: L113.

DIAGRAMA:
@step(depends_on=["step1"])
"""

from wpipe import Pipeline, step, AutoRegister


@step(name="iniciar", tags=["inic"])
def iniciar(data):
    print("🔑 Paso 1: Iniciar")
    return {"iniciado": True}


@step(name="validar", depends_on=["iniciar"], tags=["proc"])
def validar(data):
    print("✅ Paso 2: Validar (depende de iniciar)")
    return {"validado": True}


if __name__ == "__main__":
    print(">>> AutoRegister con dependencias...")

    pipe = Pipeline(pipeline_name="Viaje_L114", verbose=True)
    AutoRegister.register_all(pipe)

    pipe.set_steps([iniciar, validar])
    pipe.run({})
