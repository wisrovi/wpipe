"""
Module for printing the fuel level.
"""

from typing import Dict, Any
from wpipe import timeout_sync, to_obj


@timeout_sync(seconds=2)
@to_obj
def print_fuel_level(data: Any) -> Dict[str, Any]:
    """Print the car fuel and oil levels.

    Args:
        data (Any): Car data.

    Returns:
        Dict[str, Any]: Empty result.
    """
    print(
        f"    Fuel level: {data.fuel_level}",
        "- Oil level:",
        data.oil_level,
    )
    return {}
