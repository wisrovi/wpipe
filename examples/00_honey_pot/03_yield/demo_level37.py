"""
DEMO LEVEL 37: Shutdown Protocols (Hooks)
-----------------------------------------
Adds: Events with associated steps for post-pipeline execution.
Accumulates: Error Management (L11).

DIAGRAM:
(Trip Execution) -- [Success or Failure] --> (Trigger Hooks)
      |
      v
(send_trip_summary) -> (shutdown_ai_systems)
"""

from typing import Any, Dict
from wpipe import Pipeline, step

@step(name="drive_final_stretch")
def drive_final_stretch(data: Any) -> Dict[str, str]:
    """Final stretch driving step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Arrival status.
    """
    print("🚗 Driving the last few meters...")
    return {"arrival": "Parking"}

@step(name="shutdown_protocol")
def shutdown_protocol(data: Any) -> Dict[str, bool]:
    """Shutdown protocol step for cleaning up resources.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Shutdown status.
    """
    print("🧹 SAFETY HOOK: Deactivating cameras and clearing temporary memory...")
    return {"systems_asleep": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="safety_hooks_l37", verbose=True)

    # NEW IN L37: This event ensures shutdown_protocol runs AT THE END
    pipe.add_event(
        event_type="cleanup", event_name="End of Journey", steps=[shutdown_protocol]
    )

    pipe.set_steps([drive_final_stretch])
    print(">>> Starting trip. Safety protocols will trigger upon completion.")
    pipe.run({})
