"""
Module for driving the car.
"""

from typing import Dict, Any
from dto.car import Car, Levels
from wpipe import step, timeout_sync, to_obj


@step(
    name="drive",
    version="v1.0",
    timeout=10,
    description="Drive the car",
    tags=["trip", "car"],
    retry_count=3,
    retry_delay=0.01,
)
@timeout_sync(seconds=2)
@to_obj
def drive(my_car: Car) -> Dict[str, Any]:
    """Drive the car and consume fuel.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated car status.
    """
    if my_car.fuel_level == Levels.HIGH:
        my_car.fuel_level = Levels.MEDIUM
    elif my_car.fuel_level == Levels.MEDIUM:
        my_car.fuel_level = Levels.LOW
    elif my_car.fuel_level == Levels.LOW:
        my_car.fuel_level = Levels.EMPTY

    return {
        "fuel_level": my_car.fuel_level,
        "oil_level": Levels.LOW,
        "make": my_car.make,
    }
