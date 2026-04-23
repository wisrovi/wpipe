"""
DEMO LEVEL 12: Stereoscopic Vision (Parallel)
---------------------------------------------
Adds: Parallel processing of the Front and Rear cameras.
Accumulates: ADAS Systems (L10).

DIAGRAM:
(process_trip)
      |
   Parallel(sensors) {
      |-- (front_camera) -> [Detections ahead]
      |-- (rear_camera) -> [Detections behind]
   }
      |
      v
(data_fusion) -> [360° Map]
"""

import time
from typing import Any, Dict

from wpipe import Parallel, Pipeline, step, to_obj

@step(name="front_camera")
def front_camera(data: Any) -> Dict[str, str]:
    """Front camera processing step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Detection results for the front view.
    """
    time.sleep(0.1)
    print("🔭 Looking ahead: Road clear.")
    return {"frontal": "Clear"}

@step(name="rear_camera")
def rear_camera(data: Any) -> Dict[str, str]:
    """Rear camera processing step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Detection results for the rear view.
    """
    time.sleep(0.1)
    print("🔭 Looking back: Vehicle approaching.")
    return {"trasera": "Car at 20m"}

@step(name="fusion_360")
@to_obj
def fusion_360(ctx: Any) -> Dict[str, bool]:
    """Fuses data from all cameras into a 360 map.

    Args:
        ctx: Input context (converted to object by @to_obj).

    Returns:
        Dict[str, bool]: Safety status of the environment.
    """
    print(f"🤖 AI Fusion: Front={ctx.frontal} | Rear={ctx.trasera}")
    return {"entorno_seguro": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l12_vision360", verbose=True)
    pipe.set_steps(
        [Parallel(steps=[front_camera, rear_camera], max_workers=2), fusion_360]
    )
    pipe.run({})
