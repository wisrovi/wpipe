"""
DEMO LEVEL 14: Service Area Stop (Checkpoints)
----------------------------------------------
Adds: Saving trip status at a stop.
Accumulates: All trip telemetry.

DIAGRAM:
(Section 1: City) -> (Arrival Service Area)
      |
      v
[CHECKPOINT: 'break_1'] --> (Saves Gasoline, Km, Destination in DB)
      |
      v
(Section 2: Highway)
"""

import os
from typing import Any, Dict

from wpipe import CheckpointManager, Pipeline, step

@step(name="drive_to_service_area")
def drive_to_service_area(data: Any) -> Dict[str, int]:
    """Drive to service area step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, int]: Kilometers and gasoline level.
    """
    print("🛣️  Driving 100km to the service area...")
    return {"km": 100, "gasoline": 70}

@step(name="service_break")
def service_break(data: Any) -> Dict[str, bool]:
    """Service break step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Resting status.
    """
    print("☕ Taking a coffee. The car saves progress automatically.")
    return {"rested": True}

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    ck_mgr = CheckpointManager("output/trip_progress.db")

    pipe = Pipeline(pipeline_name="trip_l14_checkpoints", verbose=True)
    pipe.set_steps([drive_to_service_area, service_break])

    # The system registers the milestone 'stop_1'
    pipe.run(
        {"trip_id": "vacation_2026"}, checkpoint_mgr=ck_mgr, checkpoint_id="trip_1"
    )
