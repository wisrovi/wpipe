"""
DEMO LEVEL 38: Hybrid Resource Management
------------------------------------------
Adds: Combination of threads and processes for maximum efficiency.
Accumulates: Total Parallelism (L25).

DIAGRAM:
[Threads]   -> (Air Sensors, Temperature, Humidity) -> Light
[Processes] -> (4K Object Recognition AI)          -> Heavy
"""

import time
from typing import Any, Dict
from wpipe import Pipeline, step, Parallel

@step(name="heavy_ai_4k")
def heavy_ai_4k(data: Any) -> Dict[str, str]:
    """Heavy 4K video analysis step using multiprocess power.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Video analysis status.
    """
    time.sleep(0.3)
    return {"video_analyzed": "OK"}

@step(name="light_air_sensor")
def light_air_sensor(data: Any) -> Dict[str, str]:
    """Light air quality sensor step using threads.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Air quality status.
    """
    return {"air_quality": "Excellent"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="hybrid_power_l38", verbose=True)

    pipe.set_steps(
        [
            # 1. Use processes for heavy video load
            Parallel(steps=[heavy_ai_4k] * 2, use_processes=True, max_workers=2),
            # 2. Use threads for sensors that consume minimal CPU
            Parallel(steps=[light_air_sensor] * 4, use_processes=False, max_workers=4),
        ]
    )

    print(">>> Optimizing hardware: The car uses threads and processes according to the task.")
    pipe.run({})
