"""
Module for inflating car tires.
"""

from typing import Dict, Any
from dto.car import Car, Levels
from wpipe import step, to_obj


@step(name="inflate_tires", version="v1.0")
@to_obj
def inflate_tires(my_car: Car) -> Dict[str, Any]:
    """Inflate car tires to high level.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated tire level and car make.
    """
    return {
        "tire_level": Levels.HIGH,
        "make": my_car.make,
    }
