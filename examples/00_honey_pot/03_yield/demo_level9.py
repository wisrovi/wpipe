"""
DEMO LEVEL 9: YOLO Inference (Simulated)
----------------------------------------
Adds: Generation of complex predictions (dictionaries).

DIAGRAM:
(process_frame)
      |
      v
(yolo_inference) -> Generates {'prediction': {'class': 'Car', ...}}
      |
      v
(Condition) -> Reacts to the prediction
"""

import random
from typing import Any, Dict, Generator, Tuple
import numpy as np
from wpipe import Condition, For, Pipeline, step, to_obj


def simulate_video() -> Generator[Tuple[int, np.ndarray], None, None]:
    """Simulate video stream.

    Yields:
        Tuple[int, np.ndarray]: Frame ID and image.
    """
    for i in range(10):
        yield i, np.zeros((100, 100, 3), dtype=np.uint8)


@step(name="start_camera")
def start_camera(_data: Dict[str, Any]) -> Dict[str, Any]:
    """Start camera.

    Args:
        _data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Stream.
    """
    return {"stream": simulate_video()}


@step(name="process_frame")
def process_frame(data: Dict[str, Any]) -> Dict[str, Any]:
    """Process frame from stream.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Frame ID.
    """
    frame_id, _ = next(data["stream"])
    return {"frame_id": frame_id}


@step(name="yolo_inference")
@to_obj
def yolo_inference(_ctx: Any) -> Dict[str, Any]:
    """Simulate YOLO AI inference.

    Args:
        _ctx (Any): The context object.

    Returns:
        Dict[str, Any]: Detection status and AI info.
    """
    something_detected = random.random() < 0.5
    if something_detected:
        pred = {"class": "Pedestrian", "conf": 0.95}
        print(f"🔍 YOLO: Detected {pred['class']} ({pred['conf']})")
        return {"detected": True, "ai_info": pred}
    return {"detected": False, "ai_info": None}


@step(name="security_alert")
def security_alert(data: Dict[str, Any]) -> Dict[str, Any]:
    """Issue a security alert.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Empty dict.
    """
    obj = data["ai_info"]["class"]
    print(f"⚠️ ALERT: {obj} in the path!")
    return {}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L9", verbose=True)
    pipeline.set_steps(
        [
            start_camera,
            For(
                iterations=5,
                steps=[
                    process_frame,
                    yolo_inference,
                    Condition(
                        expression="detected == True", branch_true=[security_alert]
                    ),
                ],
            ),
        ]
    )
    pipeline.run({})
