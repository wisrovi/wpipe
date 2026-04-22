"""
DEMO LEVEL 112: AutoRegister por Tag
---------------------------------
Añade: Registro filtrado por tags.
Continúa: L111.

DIAGRAMA:
register_by_tag(pipeline, "inic")
"""

from wpipe import Pipeline, step, AutoRegister


@step(name="iniciar", tags=["inic"])
def iniciar(data):
    print("🔑 Iniciando...")
    return {"estado": "iniciado"}


@step(name="verificar", tags=["inic"])
def verificar(data):
    print("✅ Verificando...")
    return {"verificado": True}


if __name__ == "__main__":
    print(">>> Registro por tag...")

    pipe = Pipeline(pipeline_name="Viaje_L112", verbose=True)
    AutoRegister.register_by_tag(pipe, "inic")

    pipe.set_steps([iniciar, verificar])
    pipe.run({})
