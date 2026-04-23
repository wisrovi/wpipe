"""
Module for changing the car oil.
"""

from typing import Dict, Any
from dto.car import Car, Levels
from wpipe import step, to_obj


@step(name="change_oil", version="v1.0")
@to_obj
def change_oil(my_car: Car) -> Dict[str, Any]:
    """Change the car oil to high level.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated oil level and car make.
    """
    return {
        "oil_level": Levels.HIGH,
        "make": my_car.make,
    }
