"""
DEMO LEVEL 130: API Completo (Demo Final)
-----------------------------------
Adds: Final demo integrating everything.
Continues: L129.

DIAGRAM:
Demo completo de API con pipeline
"""

from wpipe import Pipeline, step, Metric
from wpipe.api_client import APIClient

@step(name="start")
def start(data: dict) -> None:

    """Start step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("🔑 Starting API system...")
    return {"iniciado": True}

@step(name="process")
def process(data: dict) -> None:

    """Process step.

    Args:

        data: Input data for the step.

    Returns:

        dict: Result of the step.

    """
    print("⚡ Processing data...")
    Metric.record("api_calls", 1)
    return {"procesado": True}

if __name__ == "__main__":
    print("=" * 50)
    print("🎉 DEMO FINAL - API Integration")
    print("=" * 50)

    pipe = Pipeline(pipeline_name="viaje_l130", verbose=True)
    pipe.set_steps([start, process])
    pipe.run({})

    print("\n✅ Demo completed with success!")
    print(f"📊 Metric: api_calls = 1")
