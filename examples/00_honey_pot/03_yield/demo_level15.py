"""
DEMO LEVEL 15: Resumption after Breakdown (Resume)
--------------------------------------------------
Adds: Automatic recovery from the last checkpoint.
Accumulates: Persistence (L14).

DIAGRAM:
[Breakdown detected?] -> [Load last Checkpoint]
      |
      v
(Skip steps already done) -> (Continue from point of failure)
"""

import random
from typing import Any, Dict

from wpipe import CheckpointManager, Pipeline, step

@step(name="preparation_phase")
def preparation_phase(data: Any) -> Dict[str, str]:
    """Preparation phase step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Current location.
    """
    print("🏠 Leaving home (Step already done in the past)...")
    return {"location": "road"}

@step(name="critical_phase")
def critical_phase(data: Any) -> Dict[str, str]:
    """Critical phase step with potential failure.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Trip status.

    Raises:
        RuntimeError: If a breakdown occurs.
    """
    if random.random() < 0.7:
        print("💥 ELECTRICAL BREAKDOWN! The system is shutting down.")
        raise RuntimeError("Battery failure")
    print("🏁 Arrival at final destination.")
    return {"status": "Arrived"}

if __name__ == "__main__":
    ck_mgr = CheckpointManager("output/trip_emergency.db")
    session = "return_trip"

    pipe = Pipeline(pipeline_name="trip_l15_recovery", verbose=True)
    pipe.set_steps([preparation_phase, critical_phase])

    print(f">>> Can we resume previous trip? {ck_mgr.can_resume(session)}")
    try:
        pipe.run({}, checkpoint_mgr=ck_mgr, checkpoint_id=session)
    except RuntimeError:
        print("\n[!] The car has stopped. Run again to resume.")
