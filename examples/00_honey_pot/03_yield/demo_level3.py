"""
DEMO LEVEL 3: Warehouse as Object (@to_obj)
-------------------------------------------
Adds: Use of @to_obj to access the warehouse using dot notation ('.').

DIAGRAM:
[Initial Warehouse]
      |
      v
(start_engine) ----> [engine: 'ON', fuel: 100]
      |
      v
(check_brakes @step) -> [brakes: 'OK']
      |
      v
(validate_status @to_obj) -> Accesses ctx.engine and ctx.brakes!
"""

from typing import Any, Dict
from wpipe import Pipeline, step, to_obj


def start_engine(data: Dict[str, Any]) -> Dict[str, Any]:
    """Start the car engine.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Updated context with engine status and fuel.
    """
    print(f"🔑 Engine started. Input data: {data}")
    return {"engine": "ON", "fuel": 100}


@step(name="check_brakes")
def check_brakes(data: Dict[str, Any]) -> Dict[str, Any]:
    """Verify the brakes.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Updated context with brake status.
    """
    print(f"👟 Brakes verified. Input data: {data}")
    return {"brakes": "OK"}


@step(name="validate_status")
@to_obj
def validate_status(ctx: Any) -> Dict[str, Any]:
    """Cleanly access previous data using dot notation.

    Args:
        ctx (Any): The context object allowing dot notation access.

    Returns:
        Dict[str, Any]: Confirmation that everything is ready.
    """
    if ctx.engine == "ON" and ctx.brakes == "OK":
        print(f"✅ Warehouse verified. Fuel: {ctx.fuel}%")
    return {"everything_ready": True}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L3", verbose=True)
    pipeline.set_steps([start_engine, check_brakes, validate_status])
    pipeline.run({})
