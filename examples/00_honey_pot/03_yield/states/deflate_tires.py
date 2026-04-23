"""
Module for deflating car tires.
"""

from typing import Dict, Any
from dto.car import Car, Levels
from wpipe import step, to_obj


@step(name="deflate_tires", version="v1.0")
@to_obj
def deflate_tires(my_car: Car) -> Dict[str, Any]:
    """Deflate the car tires.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated tire level and car make.
    """
    if my_car.tire_level == Levels.HIGH:
        my_car.tire_level = Levels.MEDIUM
    elif my_car.tire_level == Levels.MEDIUM:
        my_car.tire_level = Levels.LOW
    elif my_car.tire_level == Levels.LOW:
        my_car.tire_level = Levels.EMPTY

    return {
        "tire_level": my_car.tire_level,
        "make": my_car.make,
    }
