"""
DEMO LEVEL 5: Dynamic Initial Warehouse
---------------------------------------
Adds: Data injection when starting the pipeline (run).

DIAGRAM:
[Warehouse with 'weather': 'Sunny'] <--- Injected in run()
      |
      v
(Steps 1-4) --> [engine, gps, etc.]
      |
      v
(adjust_climate) -> Uses the data injected at the start!
"""

from typing import Any, Dict
from wpipe import Pipeline, step, to_obj


def start_engine(_data: Dict[str, Any]) -> Dict[str, Any]:
    """Start the engine.

    Args:
        _data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Engine status.
    """
    return {"engine": "ON"}


@step(name="configure_gps")
class ConfigureGPS:
    """Class-based step for GPS configuration."""

    def __init__(self, destination: str):
        """Initialize with destination.

        Args:
            destination (str): Destination name.
        """
        self.destination = destination

    def __call__(self, _data: Dict[str, Any]) -> Dict[str, Any]:
        """Return the destination.

        Args:
            _data (Dict[str, Any]): The current pipeline context data.

        Returns:
            Dict[str, Any]: Destination.
        """
        return {"destination": self.destination}


@step(name="adjust_climate")
@to_obj
def adjust_climate(ctx: Any) -> Dict[str, Any]:
    """Adjust the car climate based on external weather.

    Args:
        ctx (Any): The context object.

    Returns:
        Dict[str, Any]: Internal temperature setting.
    """
    # 'weather' comes from the initial dictionary in run()
    print(f"🌡️ External weather: {ctx.weather}. Adjusting air...")
    return {"internal_climate": 22}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L5", verbose=True)
    pipeline.set_steps([start_engine, ConfigureGPS("Madrid"), adjust_climate])

    # PASS INITIAL DATA HERE:
    pipeline.run({"weather": "Sunny"})
