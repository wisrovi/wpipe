"""
Module for refueling the car.
"""

from typing import Any, Dict

from dto.car import Car, Levels

from wpipe import PipelineContext, step, timeout_sync, to_obj


class TripContext(PipelineContext):
    """Context for the trip pipeline."""

    make: str
    model: str
    fuel_level: str
    oil_level: str
    tire_level: str


@timeout_sync(seconds=2)
@step(name="refuel", version="v1.0", parallel=True)
@to_obj(TripContext)
def refuel(my_car: Car) -> Dict[str, Any]:
    """Refuel the car to high level.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated fuel level and car make.
    """
    return {
        "fuel_level": Levels.HIGH,
        "make": my_car.make,
    }
