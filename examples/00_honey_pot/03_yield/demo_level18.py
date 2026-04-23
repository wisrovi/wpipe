"""
DEMO LEVEL 18: The Route Book (Exporting)
-----------------------------------------
Adds: PipelineExporter to save history to disk.
Accumulates: Data tracking (L14).

DIAGRAM:
(Trip Finished) -> [Tracking Database]
      |
      v
(PipelineExporter) -> [trip_logs.csv]
"""

import os
from typing import Any, Dict

from wpipe import Pipeline, PipelineExporter, step

@step(name="drive_section_a")
def drive_section_a(data: Any) -> Dict[str, Any]:
    """Driving section A step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, Any]: Section details.
    """
    print("🚗 Driving through Section A...")
    return {"section": "A", "duration": 15}

if __name__ == "__main__":
    db_path = "output/trip_history.db"
    os.makedirs("output", exist_ok=True)

    pipe = Pipeline(
        pipeline_name="trip_l18_exporter", tracking_db=db_path, verbose=True
    )
    pipe.set_steps([drive_section_a])
    pipe.run({})

    # NEW IN L18: Exporting the trip to a human-readable format
    print("\n>>> Generating CSV report for the insurance company...")
    exporter = PipelineExporter(db_path)
    exporter.export_pipeline_logs("output/trip_report.csv", export_format="csv")
    print("✅ Report saved in output/trip_report.csv")
