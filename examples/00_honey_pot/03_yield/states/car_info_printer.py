"""
Module for printing car information using classes and pipelines.
"""

from typing import Dict, Any, Optional
from wpipe import to_obj, Pipeline
from wpipe.decorators import step, AutoRegister, get_step_registry


@step(name="car_info_printer", version="v1.0")
class CarInfoPrinter:
    """Class to print car information."""

    def __init__(self, info: str, loop_iteration_key: Optional[str] = None):
        """Initialize the printer.

        Args:
            info (str): Information to print.
            loop_iteration_key (Optional[str]): Key for loop iteration.
        """
        self.info = info
        self.loop_iteration_key = loop_iteration_key
        self.name = "car_info_printer"
        self.version = "v1.0"

    @to_obj
    def __call__(self, data: Any) -> Dict[str, Any]:
        """Call the printer.

        Args:
            data (Any): Data to print.

        Returns:
            Dict[str, Any]: Empty result.
        """
        if self.loop_iteration_key:
            iteration = getattr(data, self.loop_iteration_key, "N/A")
            print(f"{self.info} (Iteration: {iteration})")
        else:
            print(f"{self.info}")
        return {}


@step(name="car_info_printer_2", version="v1.0")
class CarInfoPrinter2:
    """Second class to print car information."""

    def __init__(self, info: str, loop_iteration_key: Optional[str] = None):
        """Initialize the printer.

        Args:
            info (str): Information to print.
            loop_iteration_key (Optional[str]): Key for loop iteration.
        """
        self.info = info
        self.loop_iteration_key = loop_iteration_key
        self.name = "car_info_printer_2"
        self.version = "v1.0"

    @to_obj
    def __call__(self, data: Any) -> Dict[str, Any]:
        """Call the printer.

        Args:
            data (Any): Data to print.

        Returns:
            Dict[str, Any]: Empty result.
        """
        if self.loop_iteration_key:
            iteration = getattr(data, self.loop_iteration_key, "N/A")
            print(f"{self.info} (Iteration: {iteration})")
        else:
            print(f"{self.info}")
        return {}


registry = get_step_registry()

nested_step = Pipeline(
    pipeline_name="trip_tmp",
    verbose=False,
    tracking_db="output/wpipe_dashboard.db",
    show_progress=False,
)

AutoRegister.register_all(nested_step, registry)
