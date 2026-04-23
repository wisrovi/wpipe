"""
DEMO LEVEL 21: Timeouts (Response Safety)
-----------------------------------------
Adds: Timeout parameter to prevent system lockups.
Accumulates: Inference (L10) and Error Capture (L11).

DIAGRAM:
(proximity_radar) -- [Takes more than 0.2s?] -- ABORT!
      |
      v
(safety_alarm) -> [Error: Timeout]
"""

import time
from typing import Any, Dict

from wpipe import Pipeline, step

# NEW IN L21: Strict time limit for the sensor
@step(name="proximity_radar", timeout=0.2)
def proximity_radar(data: Any) -> Dict[str, bool]:
    """Proximity radar scanning step with timeout.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Obstacle detection status.
    """
    print("📡 Radar: Scanning environment...")
    # Simulate radar hardware hanging
    time.sleep(1.0)
    return {"obstacle": False}

def emergency_report(context: Dict[str, Any], error: Dict[str, Any]) -> Dict[str, Any]:
    """Emergency report handler for sensor timeouts.

    Args:
        context: Current pipeline context.
        error: Error details.

    Returns:
        Dict[str, Any]: Updated context.
    """
    print(f"\n🚨 CRITICAL ALERT: The sensor '{error['step_name']}' is not responding.")
    print("🛑 ACTION: Switching to manual driving mode.\n")
    return context

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l21_timeout", verbose=True)
    pipe.add_error_capture([emergency_report])

    pipe.set_steps([proximity_radar])

    print(">>> Safety test: Checking that the radar doesn't block the system...")
    pipe.run({})
