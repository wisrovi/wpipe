"""
DEMO LEVEL 1: The Beginning (Simple Functions)
----------------------------------------------
This level demonstrates the creation of a Pipeline and the execution
of a basic sequential function.

DIAGRAM:
[Empty Warehouse]
      |
      v
(start_engine) --> [engine: 'ON', fuel: 100]
"""

from typing import Any, Dict
from wpipe import Pipeline


def start_engine(data: Dict[str, Any]) -> Dict[str, Any]:
    """Start the car engine and initialize fuel levels.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Updated context with engine status and fuel.
    """
    print(f"🔑 Turning key: Engine started. Input data: {data}")
    return {"engine": "ON", "fuel": 100}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L1", verbose=True)
    pipeline.set_steps([start_engine])
    pipeline.run({})
