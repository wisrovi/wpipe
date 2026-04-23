"""
Car DTO module for the yield example.
Provides multiple ways to define a Car object (Pydantic, Dataclass, Traditional).
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

try:
    from pydantic import BaseModel  # pip install pydantic

    HAS_PYDANTIC = True
except ImportError:

    class BaseModel:
        """Fallback for Pydantic BaseModel."""

        def model_dump(self) -> Dict[str, Any]:
            """Dump model to dict."""
            return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    HAS_PYDANTIC = False


class Levels:
    """Standard levels for car fluids and tires."""

    EMPTY = "Empty"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


# case 1: Using Pydantic
class Extras(BaseModel):
    """Car extras using Pydantic."""

    air_conditioning: bool = True
    radio: bool = True
    gps: bool = True
    heated_seats: bool = False
    sunroof: bool = False


class Car(BaseModel):
    """Car DTO using Pydantic."""

    make: str
    model: str
    year: int = 2020
    color: str = "Red"
    fuel_level: str = Levels.MEDIUM
    oil_level: str = Levels.MEDIUM
    tire_level: str = Levels.MEDIUM
    extras: Extras = Extras()


# case 2: Using dataclass
@dataclass
class Extras2:
    """Car extras using dataclass."""

    air_conditioning: bool = True
    radio: bool = True
    gps: bool = True
    heated_seats: bool = False
    sunroof: bool = False


@dataclass
class Car2:
    """Car DTO using dataclass."""

    make: str
    model: str
    year: int = 2020
    color: str = "Red"
    fuel_level: str = Levels.MEDIUM
    oil_level: str = Levels.MEDIUM
    tire_level: str = Levels.MEDIUM
    extras: Optional[Extras2] = None

    def __post_init__(self):
        """Initialize extras if not provided."""
        if self.extras is None:
            self.extras = Extras2()


# case 3: Using traditional class
class Extras3:
    """Car extras using traditional class."""

    def __init__(self):
        """Initialize traditional extras."""
        self.air_conditioning: bool = True
        self.radio: bool = True
        self.gps: bool = True
        self.heated_seats: bool = False
        self.sunroof: bool = False


class Car3:
    """Car DTO using traditional class."""

    def __init__(
        self,
        make: str,
        model: str,
        year: int = 2020,
        color: str = "Red",
        fuel_level: str = Levels.MEDIUM,
        oil_level: str = Levels.MEDIUM,
        tire_level: str = Levels.MEDIUM,
        extras: Optional[Extras3] = None,
    ):
        """Initialize traditional car."""
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.fuel_level = fuel_level
        self.oil_level = oil_level
        self.tire_level = tire_level
        self.extras = extras if extras is not None else Extras3()


def traditional_to_dict() -> Dict[str, Any]:
    """Create a car representation using a traditional dictionary.

    Returns:
        Dict[str, Any]: Dictionary representation of a car.
    """
    return {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2021,
        "color": "Blue",
        "fuel_level": Levels.MEDIUM,
        "oil_level": Levels.MEDIUM,
        "tire_level": Levels.MEDIUM,
        "extras": {
            "air_conditioning": True,
            "radio": True,
            "gps": True,
            "heated_seats": False,
            "sunroof": False,
        },
    }


if __name__ == "__main__":
    from utils.dict2obj import to_dict

    car_pydantic = Car(make="Toyota", model="Corolla")
    car_dataclass = Car2(make="Toyota", model="Corolla")
    car_traditional = Car3(make="Toyota", model="Corolla")
    car_dict = traditional_to_dict()

    cars_to_process: List[Union[Car, Car2, Car3, Dict[str, Any]]] = [
        car_pydantic,
        car_dataclass,
        car_traditional,
        car_dict,
    ]

    for i, car_obj in enumerate(cars_to_process, 1):
        try:
            processed_dict = to_dict(car_obj)
        except TypeError as exc:
            raise ValueError(
                f"Object type {type(car_obj).__name__} is not compatible for dict conversion"
            ) from exc

        print(f"Result {i}: {processed_dict}")
