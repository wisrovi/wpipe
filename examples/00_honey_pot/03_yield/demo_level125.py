"""
DEMO LEVEL 125: Pipeline con API
---------------------------------
Adds: Pipeline que usa API.
Continues: L124.

DIAGRAM:
Pipeline + APIClient
"""

from wpipe import Pipeline, step
from wpipe.api_client import APIClient

@step(name="fetch_data")
def fetch_data(data: dict) -> None:

    """Fetch data step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("📥 Obteniendo datos de API...")
    return {"datos": [1, 2, 3]}

if __name__ == "__main__":
    print(">>> Pipeline con API...")

    pipe = Pipeline(pipeline_name="viaje_l125", verbose=True)
    pipe.set_steps([fetch_data])
    pipe.run({})
