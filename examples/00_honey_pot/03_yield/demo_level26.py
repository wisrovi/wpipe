"""
DEMO LEVEL 26: The Central Screen (Dashboard)
---------------------------------------------
Adds: Connection with the tracking database for visualization.
Accumulates: YOLO Inference and Telemetry.

DIAGRAM:
(Process Trip) -> [SQLite Database]
      |
      +----------> [Web Dashboard] -> (Charts, Times, Alerts)
"""

import os
from typing import Any, Dict

from wpipe import Pipeline, step

@step(name="active_navigation")
def active_navigation(data: Any) -> Dict[str, str]:
    """Active navigation step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Navigation details.
    """
    print("🗺️  Navigation: Guiding to destination... (Data being recorded for the Dashboard)")
    return {"stretch": "Highway A-6"}

if __name__ == "__main__":
    db_path = "output/car_dashboard.db"
    os.makedirs("output", exist_ok=True)

    # NEW IN L26: By defining tracking_db, we enable the car's 'Black Box'
    pipe = Pipeline(pipeline_name="adas_system_l26", tracking_db=db_path, verbose=True)

    pipe.set_steps([active_navigation])

    print(f">>> TIP: Open a terminal and run 'wpipe dashboard {db_path}'")
    pipe.run({})
