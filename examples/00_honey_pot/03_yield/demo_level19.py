"""
DEMO LEVEL 19: Modular Sections (Nested Pipelines)
--------------------------------------------------
Adds: Use of a Pipeline as a step of another.
Accumulates: Modularization of driving.

DIAGRAM:
Pipeline(Full Trip) [
  (Engine Preparation)
  Pipeline(Urban_Section) [
     (Pass Traffic Lights)
     (Pedestrian Control)
  ]
  (Arrival)
]
"""

from typing import Any, Dict
from wpipe import Pipeline, step

@step(name="prepare_engine")
def prepare_engine(data: Any) -> Dict[str, str]:
    """Engine preparation step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Engine status.
    """
    return {"engine": "READY"}

# NEW IN L19: Defining an independent 'sub-trip'
urban_section = Pipeline(pipeline_name="urban_driving")

@step(name="cross_crosswalk")
def cross_crosswalk(data: Any) -> Dict[str, bool]:
    """Cross crosswalk step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Pedestrian status.
    """
    print("🚶 Urban Section: Yielding to pedestrians...")
    return {"pedestrians_crossing": False}

urban_section.set_steps([cross_crosswalk])

if __name__ == "__main__":
    full_trip = Pipeline(pipeline_name="trip_l19_modular", verbose=True)

    full_trip.set_steps(
        [
            prepare_engine,
            urban_section,  # <--- The urban pipeline acts as a piece of the trip
            (lambda d: print("🏁 Trip completed."), "finish", "v1"),
        ]
    )

    full_trip.run({})
