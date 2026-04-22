"""
DEMO LEVEL 111: AutoRegister
------------------------------
Añade: Registro automático de steps.
Continúa: Wsqlite de L110.

DIAGRAMA:
@step + AutoRegister.register_all()
"""

from wpipe import Pipeline, step, AutoRegister


@step(name="iniciar", tags=["inic"])
def iniciar(data):
    print("🔑 Iniciando...")
    return {"estado": "iniciado"}


@step(name="procesar", tags=["proc"])
def procesar(data):
    print("⚡ Procesando...")
    return {"procesado": True}


if __name__ == "__main__":
    print(">>> AutoRegister...")

    pipe = Pipeline(pipeline_name="Viaje_L111", verbose=True)
    AutoRegister.register_all(pipe)

    pipe.set_steps([iniciar, procesar])
    pipe.run({})
