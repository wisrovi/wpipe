"""
DEMO LEVEL 29: Safety Save (Smart Checkpoints)
----------------------------------------------
Adds: Checkpoints that only fire under critical conditions.
Accumulates: Persistence (L14).

DIAGRAM:
(Trip) -> [Fuel < 15%?] -- YES --> (Save Rescue Point)
"""

import os
from typing import Any, Dict

from wpipe import CheckpointManager, Pipeline, step

@step(name="critical_consumption")
def critical_consumption(data: Any) -> Dict[str, int]:
    """Critical consumption detection step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, int]: Fuel level.
    """
    # Simulate fuel dropping dangerously
    fuel_actual = 10
    print(f"⛽ Fuel Alert: {fuel_actual}%")
    return {"fuel": fuel_actual}

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    ck_mgr = CheckpointManager("output/car_safety.db")
    pipe = Pipeline(pipeline_name="safety_first_l29", verbose=True)

    # NEW IN L29: The car saves automatically only if fuel is low
    pipe.add_checkpoint(checkpoint_name="rescue_point", expression="fuel < 15")

    pipe.set_steps([critical_consumption])
    pipe.run({"fuel": 100}, checkpoint_mgr=ck_mgr, checkpoint_id="night_trip")
