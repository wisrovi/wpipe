"""
DEMO LEVEL 27: Efficiency Log (Metrics)
---------------------------------------
Adds: Real-time numerical metrics recording.
Accumulates: Dashboard (L26).

DIAGRAM:
(drive)
   |-- Metric.record("consumption") -> 6.5 L
   |-- Metric.record("speed") -> 120 km/h
"""

import random
from typing import Any, Dict

from wpipe import Metric, Pipeline, step

@step(name="measure_efficiency")
def measure_efficiency(data: Any) -> Dict[str, float]:
    """Measure efficiency step recording fuel and speed metrics.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, float]: Efficiency data.
    """
    consumption = random.uniform(5.5, 9.0)
    speed = random.randint(100, 130)

    # NEW IN L27: Record numerical data for subsequent analytics
    Metric.record("fuel_consumption", consumption, unit="L/100km")
    Metric.record("average_speed", speed, unit="km/h")

    print(f"📊 Telemetry: {speed} km/h | {consumption:.1f} L/100km")
    return {"fuel": consumption, "speed": float(speed)}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="trip_efficiency_l27",
        tracking_db="output/car_telemetry.db",
        verbose=True,
    )
    pipe.set_steps([measure_efficiency])
    pipe.run({})
