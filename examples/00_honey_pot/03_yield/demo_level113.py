"""
DEMO LEVEL 113: AutoRegister Múltiples Tags
-----------------------------------------
Añade: Registro con múltiples tags.
Continúa: L112.

DIAGRAMA:
registros con diferentes tags
"""

from wpipe import Pipeline, step, AutoRegister


@step(name="iniciar", tags=["inic", "auto"])
def iniciar(data):
    print("🔑 Iniciando...")
    return {"estado": "iniciado"}


@step(name="procesar", tags=["proc"])
def procesar(data):
    print("⚡ Procesando...")
    return {"procesado": True}


@step(name="verificar", tags=["inic"])
def verificar(data):
    print("✅ Verificando...")
    return {"verificado": True}


if __name__ == "__main__":
    print(">>> Múltiples tags...")

    pipe = Pipeline(pipeline_name="Viaje_L113", verbose=True)
    AutoRegister.register_all(pipe)

    pipe.set_steps([iniciar, procesar, verificar])
    pipe.run({})
