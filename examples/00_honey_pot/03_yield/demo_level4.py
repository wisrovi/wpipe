"""
DEMO LEVEL 4: Configuration with Classes
-----------------------------------------
Adds: Use of Classes as steps with parameters (__init__).

DIAGRAM:
[Initial Warehouse]
      |
      v
(start_engine) --> (check_brakes) --> (validate_status)
      |
      v
(ConfigureGPS @step) -> Receives 'destination' as a parameter!
"""

from typing import Any, Dict
from wpipe import Pipeline, step, to_obj


def start_engine(_data: Dict[str, Any]) -> Dict[str, Any]:
    """Start the car engine.

    Args:
        _data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Updated context with engine status and fuel.
    """
    return {"engine": "ON", "fuel": 100}


@step(name="check_brakes")
def check_brakes(_data: Dict[str, Any]) -> Dict[str, Any]:
    """Verify the brakes.

    Args:
        _data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Updated context with brake status.
    """
    return {"brakes": "OK"}


@step(name="validate_status")
@to_obj
def validate_status(ctx: Any) -> Dict[str, Any]:
    """Validate the car status.

    Args:
        ctx (Any): The context object.

    Returns:
        Dict[str, Any]: Readiness status.
    """
    print(f"🚀 Car ready. Fuel: {ctx.fuel}%")
    return {"ready": True}


@step(name="configure_gps")
class ConfigureGPS:
    """Class-based step to configure the GPS with a destination."""

    def __init__(self, destination: str):
        """Initialize the GPS with a destination.

        Args:
            destination (str): The trip destination.
        """
        self.destination = destination

    def __call__(self, _data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate the route to the destination.

        Args:
            _data (Dict[str, Any]): The current pipeline context data.

        Returns:
            Dict[str, Any]: Destination and distance.
        """
        print(f"📍 GPS: Calculating route to {self.destination}...")
        return {"destination": self.destination, "distance": 450}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L4", verbose=True)
    pipeline.set_steps(
        [
            start_engine,
            check_brakes,
            validate_status,
            ConfigureGPS("Madrid"),
        ]
    )
    pipeline.run({})
