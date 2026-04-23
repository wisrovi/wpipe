"""
DEMO LEVEL 17: AI Engine Monitor (Resources)
--------------------------------------------
Adds: collect_system_metrics=True to watch car load.
Accumulates: Heavy inference (L13).

DIAGRAM:
[Start Monitor] ------------------+
      |                            | (Watches CPU/RAM in background)
      v                            |
(Process Neural Networks) <--------+
      |
      v
[Resource Log] -> Reports consumption peaks of the ADAS system.
"""

import time
from typing import Any, Dict

from wpipe import Parallel, Pipeline, step

@step(name="ai_vision_360")
def ai_vision_360(data: Any) -> Dict[str, str]:
    """AI Vision 360 processing step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Detection status.
    """
    print("🧠 Processing 360° artificial vision...")
    time.sleep(0.5)  # Simulate intensive processing
    return {"detections": "OK"}

if __name__ == "__main__":
    # We activate system resource monitoring
    pipe = Pipeline(
        pipeline_name="trip_l17_performance",
        verbose=True,
        collect_system_metrics=True,  # <--- NEW: Monitor hardware
    )

    pipe.set_steps([Parallel(steps=[ai_vision_360] * 4, max_workers=4)])

    print(">>> Starting trip. Observe the metrics logs when finished...")
    pipe.run({})
