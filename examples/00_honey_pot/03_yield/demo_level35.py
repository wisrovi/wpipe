"""
DEMO LEVEL 35: Multi-Object Radar (Complex Pydantic)
----------------------------------------------------
Adds: Nested AI structures and lists of objects.
Accumulates: ADAS Vision (L10) and Pydantic (L16).

DIAGRAM:
(Radar_AI) -> { 'list': [ {'type': 'Car', 'id': 1}, ... ] }
      |
      v
(Process_Radar) -> Validates each object in the list individually.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from wpipe import Pipeline, step, to_obj

class DetectedObject(BaseModel):
    """Pydantic model for a single detected object."""
    type: str
    confidence: float = Field(..., ge=0, le=1)

class RadarMap(BaseModel):
    """Pydantic model for radar detection map."""
    detections: List[DetectedObject]

@step(name="radar_yolo_pro")
def radar_yolo_pro(data: Any) -> Dict[str, List[Dict[str, Any]]]:
    """Simulates high-end YOLO radar detections.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, List[Dict[str, Any]]]: List of detected objects.
    """
    return {
        "detections": [
            {"type": "Pedestrian", "confidence": 0.98},
            {"type": "Bicycle", "confidence": 0.85},
            {"type": "Car", "confidence": 0.92},
        ]
    }

@step(name="environment_analysis")
@to_obj(RadarMap)
def environment_analysis(ctx: RadarMap) -> Dict[str, bool]:
    """Analyzes the environment based on radar detections.

    Args:
        ctx: Validated radar map context.

    Returns:
        Dict[str, bool]: Path clear status.
    """
    print(f"👁️  Radar: Identified {len(ctx.detections)} elements in trajectory.")
    for obj in ctx.detections:
        print(f"   - {obj.type} (Confidence: {obj.confidence*100:.0f}%)")
    return {"path_clear": False}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="advanced_radar_l35", verbose=True)
    pipe.set_steps([radar_yolo_pro, environment_analysis])
    pipe.run({})
