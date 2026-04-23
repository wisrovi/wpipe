"""
DEMO LEVEL 2: Metadata (@step)
------------------------------
This level introduces the use of @step to provide a name, version,
and traceability to the pipeline steps.

DIAGRAM:
[Empty Warehouse]
      |
      v
(start_engine) ----> [engine: 'ON']
      |
      v
(check_brakes @step) -> [engine: 'ON', brakes: 'OK']
"""

from typing import Any, Dict
from wpipe import Pipeline, step


def start_engine(data: Dict[str, Any]) -> Dict[str, Any]:
    """Start the car engine and initialize fuel levels.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Updated context with engine status and fuel.
    """
    print(f"🔑 Turning key: Engine started. Input data: {data}")
    return {"engine": "ON", "fuel": 100}


@step(name="check_brakes", version="v1.0")
def check_brakes(data: Dict[str, Any]) -> Dict[str, Any]:
    """Verify the state of the brake system.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Updated context with brake status.
    """
    print(f"👟 Testing pedals: Brakes verified. Input data: {data}")
    return {"brakes": "OK"}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L2", verbose=True)
    pipeline.set_steps([start_engine, check_brakes])
    pipeline.run({})
