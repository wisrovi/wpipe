"""
DEMO LEVEL 24: Total Odometer (Shared Memory)
---------------------------------------------
Adds: Use of 'memory' module for data that transcends the trip.
Accumulates: Persistence (L14).

DIAGRAM:
(Morning Trip) -> Update memory['total_km']
      |
(Afternoon Trip) -> Read memory['total_km'] and increase it
"""

from typing import Any, Dict
from wpipe import Pipeline, memory, step


@step(name="register_section")
def register_section(data: Any) -> Dict[str, int]:
    """Register trip section and update total odometer in shared memory.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, int]: Total kilometers.
    """
    section_km = 40
    # NEW IN L24: Save in persistent global RAM
    total = memory.get("car_odometer", 0) + section_km
    memory.set("car_odometer", total)

    print(f"🛣️  Section: +{section_km}km | Total Odometer in Memory: {total}km")
    return {"total_km": total}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l24_memory", verbose=True)
    pipe.set_steps([register_section])

    print(">>> Starting the car for the first time:")
    pipe.run({})
    print("\n>>> Starting the car for the second time (Memory maintained)")

    pipe.run({})
