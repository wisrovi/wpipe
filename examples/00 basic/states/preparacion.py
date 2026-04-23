"""Module for preparation phase steps."""

from typing import Dict, Any
from dto.car import Car, Levels
from wpipe import step, to_obj


@step(name="open_car", version="v1.0", description="Open the car door")
@to_obj
def open_car(my_car: Car) -> Dict[str, Any]:
    """Open the car door.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated car status and confirmation.
    """
    print("🔑 Opening car door...")
    return {"car_door": "open", "make": my_car.make}


@step(name="inflate_tires_prep", version="v1.0", description="Inflate tires to preparation level")
@to_obj
def inflate_tires_prep(my_car: Car) -> Dict[str, Any]:
    """Inflate car tires to a preparatory level.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated tire level.
    """
    print("⬆️ Inflating tires to preparation level...")
    my_car.fuel_level = Levels.MEDIUM
    return {"tire_level": Levels.PREP, "make": my_car.make}


@step(name="clean_windshield", version="v1.0", description="Clean the car windshield")
@to_obj
def clean_windshield(my_car: Car) -> Dict[str, Any]:
    """Clean the car windshield.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated windshield status.
    """
    print("🧼 Cleaning windshield...")
    return {"windshield": "clean", "make": my_car.make}


@step(name="start_motor", version="v1.0", description="Start the car engine")
@to_obj
def start_motor(my_car: Car) -> Dict[str, Any]:
    """Start the car engine.

    Args:
        my_car (Car): The car instance.

    Returns:
        Dict[str, Any]: Updated engine status.
    """
    print("🔑 Turning key: Engine started.")
    return {"engine": "ON", "make": my_car.make}


def preparation_phase(data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute the preparation phase for the trip.

    Args:
        data (Dict[str, Any]): Input data dictionary.

    Returns:
        Dict[str, Any]: Updated data dictionary after preparation.
    """
    # Initialize car if not present
    my_car = data.get("my_car", Car(make="Toyota", model="Corolla", year=2020))

    # Execute steps sequentially
    data = open_car(my_car)
    data = inflate_tires_prep(my_car)
    data = clean_windshield(my_car)
    data = start_motor(my_car)

    return data
