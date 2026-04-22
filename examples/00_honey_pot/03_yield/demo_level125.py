"""
DEMO LEVEL 125: Pipeline con API
---------------------------------
Añade: Pipeline que usa API.
Continúa: L124.

DIAGRAMA:
Pipeline + APIClient
"""

from wpipe import Pipeline, step
from wpipe.api_client import APIClient


@step(name="fetch_data")
def fetch_data(data):
    print("📥 Obteniendo datos de API...")
    return {"datos": [1, 2, 3]}


if __name__ == "__main__":
    print(">>> Pipeline con API...")

    pipe = Pipeline(pipeline_name="Viaje_L125", verbose=True)
    pipe.set_steps([fetch_data])
    pipe.run({})
