"""
DEMO LEVEL 11: Sensor Failure (Error Capture)
---------------------------------------------
Adds: Error handling when the camera gets dirty or fails.
Accumulates: Smart Windshield (L10).

DIAGRAM:
(Camera) -- [Lens dirty?] -- ERROR! --> (Automatic Windshield Wipers)
      |
      v
(Process Trip)
"""

import random
from typing import Any, Dict

from wpipe import Pipeline, step

def emergency_maintenance(context: Dict[str, Any], error: Dict[str, Any]) -> Dict[str, Any]:
    """Emergency maintenance handler when a sensor fails.

    Args:
        context: The current pipeline context.
        error: Dictionary containing error details.

    Returns:
        Dict[str, Any]: The updated context.
    """
    print(f"\n🔧 SYSTEM: Error detected in '{error['step_name']}'.")
    print("🧼 ACTION: Activating sensor self-cleaning...\n")
    return context

@step(name="verify_lens")
def verify_lens(data: Any) -> Dict[str, str]:
    """Verifies if the sensor lens is clean.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Vision status.

    Raises:
        RuntimeError: If visibility is obstructed.
    """
    if random.random() < 0.3:
        raise RuntimeError("Obstructed visibility (Dirty lens)")
    print("👀 Sensors clean. Visibility 100%.")
    return {"vision": "Clear"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l11_faulttolerance", verbose=True)

    # The car now knows what to do if vision fails
    pipe.add_error_capture([emergency_maintenance])

    pipe.set_steps([verify_lens])
    print(">>> Starting trip with security sensors...")
    pipe.run({})
