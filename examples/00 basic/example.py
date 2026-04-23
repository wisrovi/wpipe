"""
Example demonstrating a pipeline for a car journey.

This script defines a pipeline that simulates a car journey,
including steps like refueling, oil changes, driving,
and tire pressure adjustments. It uses wpipe components
like Pipeline, Condition, and For, along with custom states
and data structures for car representation.
"""

from typing import Any, Dict, List, Union

from wpipe import Condition, For, Pipeline

# Assuming 'dto.car' now contains 'Car' and 'Levels' (translated from Niveles)
# Assuming 'states' module has translated states like Refuel, ChangeOil, Drive, etc.
# Assuming 'utils.dict2obj' and 'utils.obj2dict' are available.
try:
    from dto.car import Car, Levels
except ImportError:
    # Placeholder for Car and Levels if import fails. In a real scenario, ensure paths are correct.
    print("Warning: Could not import Car and Levels from dto.car. Using placeholders.")
    class Car: # Dummy class for type hinting if import fails
        def __init__(self, make: str, model: str, **kwargs: Any):
            self.make = make
            self.model = model
            self.gasoline_level: str = "Medium"
            self.tire_level: str = "Medium"
            self.oil_level: str = "Medium"
            # Add other attributes if necessary for pipeline logic

    class Levels: # Dummy class for type hinting if import fails
        empty: str = "Empty"
        low: str = "Low"
        medium: str = "Medium"
        high: str = "High"

try:
    from states import (
        Refuel, # Translated from HecharGasolina
        ChangeOil, # Translated from cambiar_aceite
        Drive, # Translated from conducir
        DeflateTires, # Translated from desinflar_neumaticos
        InflateTires, # Translated from inflar_neumaticos
    )
except ImportError:
    # Placeholder for states if import fails
    print("Warning: Could not import states. Using placeholders.")
    # Define dummy classes/functions if states are not found, to allow script execution.
    # These placeholders would need to mimic the expected behavior for the pipeline to run.
    class Refuel:
        NAME = "Refuel"
        VERSION = "v1.0"
        def __call__(self, car: Car): print("Refueling car...")
    class ChangeOil:
        NAME = "ChangeOil"
        VERSION = "v1.0"
        def __call__(self, car: Car): print("Changing oil...")
    class Drive:
        NAME = "Drive"
        VERSION = "v1.0"
        def __call__(self, car: Car): print("Driving car...")
    class DeflateTires:
        NAME = "DeflateTires"
        VERSION = "v1.0"
        def __call__(self, car: Car): print("Deflating tires...")
    class InflateTires:
        NAME = "InflateTires"
        VERSION = "v1.0"
        def __call__(self, car: Car): print("Inflating tires...")

# Assuming utils.dict2obj and utils.obj2dict exist and are correctly imported
try:
    from utils.dict2obj import to_obj
except ImportError:
    print("Warning: Could not import to_obj from utils.dict2obj. Using placeholder.")
    def to_obj(data: Dict[str, Any]) -> Any:
        """Placeholder for to_obj if import fails."""
        class DynamicObject:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        return DynamicObject(**data)

try:
    from utils.obj2dict import auto_dict_input
except ImportError:
    print("Warning: Could not import auto_dict_input from utils.obj2dict. Using placeholder.")
    def auto_dict_input(func): # Simple decorator placeholder
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper


def main() -> None:
    """
    Sets up and runs a car journey pipeline.

    This function configures a wpipe Pipeline with various steps,
    including conditional logic and loops, to simulate a car journey.
    It then executes the pipeline with sample car data.
    """
    db_path: str = "wpipe_dashboard.db"
    config_dir: str = "configs"

    # Initialize the pipeline with English names and parameters
    journey_pipeline = Pipeline(
        pipeline_name="journey", # Changed from 'viaje' to 'journey'
        verbose=False,
        tracking_db=db_path,
        config_dir=config_dir,
    )

    # Add an event for notifications
    journey_pipeline.add_event(
        event_type="notification",
        event_name="authorized_person",
        message="Results sent to external APIs",
    )

    # Define the steps of the pipeline
    # Ensure translated state names and versions are used.
    pipeline_steps = [
        # Refuel step
        (Refuel, Refuel.NAME, Refuel.VERSION),
        # Change oil step
        (ChangeOil, ChangeOil.NAME, ChangeOil.VERSION),
        # Conditional driving and tire adjustments
        (
            For(
                # Translate validation expression to use translated Levels and Car attributes
                validation_expression="car_obj.gasoline_level != Levels.empty", # Assuming 'car_obj' will be the variable name in steps
                steps=[
                    # Drive step
                    (Drive, Drive.NAME, Drive.VERSION),
                    # Tire pressure adjustment based on condition
                    (
                        Condition(
                            # Translate expression to use translated Levels and Car attributes
                            expression="car_obj.tire_level == Levels.low", # Assuming 'car_obj' will be the variable name in steps
                            branch_true=[
                                # Inflate tires step
                                (InflateTires, InflateTires.NAME, InflateTires.VERSION),
                            ],
                            branch_false=[
                                # Deflate tires step
                                (DeflateTires, DeflateTires.NAME, DeflateTires.VERSION),
                            ],
                        )
                    ),
                    # Lambda to print gasoline level
                    (
                        lambda car_obj: print(
                            f"Gasoline level: {car_obj.gasoline_level}"
                        ),
                        "print_gasoline_level", # Renamed step name for clarity
                        "v1.0",
                    ),
                ],
            )
        ),
        # Final step to print journey completion message
        (lambda car_obj: print("Journey complete"), "print_journey_complete", "v1.0"), # Renamed step name
    ]

    journey_pipeline.set_steps(pipeline_steps)

    # Decorator to automatically handle dictionary input for the run function
    @auto_dict_input
    def run_pipeline(args_dict: Dict[str, Any]) -> Any:
        """
        Runs the configured journey pipeline.

        Args:
            args_dict: A dictionary containing arguments for the pipeline.
                       This is expected to be convertible to Car objects or similar structures.

        Returns:
            The result of the pipeline execution.
        """
        return journey_pipeline.run(args_dict)

    # --- Execute the pipeline with different car representations ---

    # 1. Using Car object (Pydantic model)
    # Note: 'make' and 'model' are already English in Car constructor after refactoring dto/car.py
    pydantic_car_instance = Car(make="Toyota", model="Corolla")
    results_pydantic = run_pipeline(pydantic_car_instance)
    print(f"Results (Pydantic Car): {results_pydantic}")

    # 2. Using dictionary representation
    # The run_pipeline function (due to @auto_dict_input and wpipe's internal handling)
    # should be able to process a dictionary and potentially convert it.
    dict_car_data_for_run = {
        "make": "Honda",
        "model": "Civic",
        "year": 2022,
        "color": "Blue",
        "gasoline_level": Levels.high,
        "tire_level": Levels.medium,
        "oil_level": Levels.medium,
        "extras": {
            "air_conditioning": True,
            "radio": True,
            "gps": True,
            "heated_seats": True,
            "sunroof": True,
        },
    }
    results_dict = run_pipeline(dict_car_data_for_run)
    print(f"Results (Dictionary): {results_dict}")

if __name__ == "__main__":
    main()
