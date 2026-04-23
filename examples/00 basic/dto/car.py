"""
Module demonstrating different ways to represent car data,
including Pydantic models, dataclasses, traditional classes,
and dictionary conversions.
"""

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel  # pip install pydantic

# Import from utils if it's available in the workspace
try:
    from utils.dict2obj import to_dict
except ImportError:
    # Provide a fallback if utils.dict2obj is not found, though ideally it should be present.
    # This fallback aims to mimic common dict2obj behavior for demonstration.
    # In a real scenario, ensure the import path is correct.
    def to_dict(obj: Any) -> Dict[str, Any]:
        """
        Fallback function to convert objects to dictionaries.
        Tries to use __dict__ or asdict if available.
        """
        if is_dataclass(obj) and not isinstance(obj, type):
            return asdict(obj)
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        raise TypeError(f"Object of type {type(obj).__name__} cannot be converted to dict")


class Levels:
    """Represents the levels for various car components."""
    empty: str = "Empty"
    low: str = "Low"
    medium: str = "Medium"
    high: str = "High"


# Case 1: Using Pydantic
class CarExtras(BaseModel):
    """
    Pydantic model for car extras.

    Attributes:
        air_conditioning: Whether the car has air conditioning.
        radio: Whether the car has a radio.
        gps: Whether the car has GPS.
        heated_seats: Whether the car has heated seats.
        sunroof: Whether the car has a sunroof.
    """
    air_conditioning: bool = True
    radio: bool = True
    gps: bool = True
    heated_seats: bool = False
    sunroof: bool = False


class Car(BaseModel):
    """
    Pydantic model representing a car.

    Attributes:
        make: The manufacturer of the car.
        model: The model of the car.
        year: The manufacturing year of the car.
        color: The color of the car.
        gasoline_level: The current level of gasoline.
        oil_level: The current level of engine oil.
        tire_level: The current level of tire pressure.
        extras: Additional features of the car.
    """
    make: str
    model: str
    year: int = 2020
    color: str = "Red"
    gasoline_level: str = Levels.medium
    oil_level: str = Levels.medium
    tire_level: str = Levels.medium
    extras: CarExtras = field(default_factory=CarExtras) # Use default_factory for BaseModel


# Case 2: Using dataclass
@dataclass
class CarExtras2:
    """
    Dataclass for car extras.

    Attributes:
        air_conditioning: Whether the car has air conditioning.
        radio: Whether the car has a radio.
        gps: Whether the car has GPS.
        heated_seats: Whether the car has heated seats.
        sunroof: Whether the car has a sunroof.
    """
    air_conditioning: bool = True
    radio: bool = True
    gps: bool = True
    heated_seats: bool = False
    sunroof: bool = False


@dataclass
class Car2:
    """
    Dataclass representing a car.

    Attributes:
        make: The manufacturer of the car.
        model: The model of the car.
        year: The manufacturing year of the car.
        color: The color of the car.
        gasoline_level: The current level of gasoline.
        oil_level: The current level of engine oil.
        tire_level: The current level of tire pressure.
        extras: Additional features of the car.
    """
    make: str
    model: str
    year: int = 2020
    color: str = "Red"
    gasoline_level: str = Levels.medium
    oil_level: str = Levels.medium
    tire_level: str = Levels.medium
    extras: Optional[CarExtras2] = None

    def __post_init__(self):
        """Initialize extras if not provided."""
        if self.extras is None:
            self.extras = CarExtras2()


# Case 3: Using traditional class
class CarExtras3:
    """
    Traditional class for car extras.

    Attributes:
        air_conditioning: Whether the car has air conditioning.
        radio: Whether the car has a radio.
        gps: Whether the car has GPS.
        heated_seats: Whether the car has heated seats.
        sunroof: Whether the car has a sunroof.
    """
    def __init__(self):
        self.air_conditioning: bool = True
        self.radio: bool = True
        self.gps: bool = True
        self.heated_seats: bool = False
        self.sunroof: bool = False


class Car3:
    """
    Traditional class representing a car.

    Attributes:
        make: The manufacturer of the car.
        model: The model of the car.
        year: The manufacturing year of the car.
        color: The color of the car.
        gasoline_level: The current level of gasoline.
        oil_level: The current level of engine oil.
        tire_level: The current level of tire pressure.
        extras: Additional features of the car.
    """
    def __init__(
        self,
        make: str,
        model: str,
        year: int = 2020,
        color: str = "Red",
        gasoline_level: str = Levels.medium,
        oil_level: str = Levels.medium,
        tire_level: str = Levels.medium,
        extras: Optional[CarExtras3] = None,
    ):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.fuel_level = fuel_level
        self.oil_level = oil_level
        self.tire_level = tire_level
        self.extras = extras if extras is not None else CarExtras3()


# Case 4: Using traditional dict
def get_traditional_car_dict() -> Dict[str, Any]:
    """
    Returns a dictionary representing a traditional car.

    Returns:
        A dictionary containing car details.
    """
    return {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2021,
        "color": "Blue",
        "fuel_level": Levels.medium,
        "oil_level": Levels.medium,
        "tire_level": Levels.medium,
        "extras": {
            "air_conditioning": True,
            "radio": True,
            "gps": True,
            "heated_seats": False,
            "sunroof": False,
        },
    }


if __name__ == "__main__":
    # Instantiate objects using different representations
    pydantic_car = Car(make="Toyota", model="Corolla")
    dataclass_car = Car2(make="Toyota", model="Corolla")
    traditional_car_obj = Car3(make="Toyota", model="Corolla")
    dict_car_data = get_traditional_car_dict()

    car_objects: list[Any] = [pydantic_car, dataclass_car, traditional_car_obj, dict_car_data]

    for i, car_obj in enumerate(car_objects, 1):
        # print(f"
--- Processing Car Object {i} ---") # Commented out as per instructions

        # Attempt to convert the object to a dictionary using the utility function
        try:
            # Check if the object is already a dict, if so, use it directly.
            if isinstance(car_obj, dict):
                car_dict_representation = car_obj
            else:
                car_dict_representation = to_dict(car_obj)
        except TypeError as e:
            # Handle cases where conversion to dict is not straightforward
            print(f"Warning: Could not convert object of type {type(car_obj).__name__} to dict: {e}")
            continue # Skip to the next object if conversion fails

        # print(f"Original object type: {type(car_obj).__name__}") # Commented out
        print(f"Dictionary representation: {car_dict_representation}")
        # print(f"Resulting dictionary type: {type(car_dict_representation).__name__}") # Commented out
out
