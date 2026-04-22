"""
DEMO LEVEL 105: States Analysis
-----------------------------
Añade: Análisis de estados.
Continúa: L104.

DIAGRAMA:
analysis.get_states_analysis()
"""

from wpipe import Pipeline, step


@step(name="iniciar")
def iniciar(data):
    return {"estado": "iniciado"}


@step(name="verificar")
def verificar(data):
    return {"verificado": True}


if __name__ == "__main__":
    print(">>> Análisis de estados...")

    pipe = Pipeline(
        pipeline_name="Viaje_L105_States",
        verbose=True,
        tracking_db="output/states105.db",
    )
    pipe.set_steps([iniciar, verificar])
    pipe.run({})

    states = pipe.tracker.analysis.get_states_analysis()
    print(f"\n📊 Estados: {states}")
