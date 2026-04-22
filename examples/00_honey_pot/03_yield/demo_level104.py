"""
DEMO LEVEL 104: Pipeline Analytics
------------------------------
Añade: Análisis completo de pipelines.
Continúa: L103.

DIAGRAMA:
analysis.get_pipelines_analysis()
"""

from wpipe import Pipeline, step


@step(name="iniciar")
def iniciar(data):
    return {"motor": "on"}


@step(name="procesar")
def procesar(data):
    return {"ok": True}


if __name__ == "__main__":
    print(">>> Análisis de pipelines...")

    pipe = Pipeline(
        pipeline_name="Viaje_L104_Pipelines",
        verbose=True,
        tracking_db="output/pipelines104.db",
    )
    pipe.set_steps([iniciar, procesar])
    pipe.run({})

    analysis = pipe.tracker.analysis.get_pipelines_analysis()
    print(f"\n📊 Análisis:")
    print(f"  Total: {len(analysis)}")
