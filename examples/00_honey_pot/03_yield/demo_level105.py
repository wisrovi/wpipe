"""
DEMO LEVEL 105: States Analysis
-----------------------------
Adds: Análisis de estados.
Continues: L104.

DIAGRAM:
analysis.get_states_analysis()
"""

from wpipe import Pipeline, step

@step(name="start")
def start(data: dict) -> None:

    """Start step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    return {"estado": "iniciado"}

@step(name="verificar")
def verificar(data: dict) -> None:

    """Verificar step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    return {"verificado": True}

if __name__ == "__main__":
    print(">>> Análisis de estados...")

    pipe = Pipeline(
        pipeline_name="viaje_l105_states",
        verbose=True,
        tracking_db="output/states105.db",
    )
    pipe.set_steps([start, verificar])
    pipe.run({})

    states = pipe.tracker.analysis.get_states_analysis()
    print(f"\n📊 Estados: {states}")
