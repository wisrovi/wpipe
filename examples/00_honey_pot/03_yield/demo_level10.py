"""
DEMO LEVEL 10: The Intelligent Windshield (HUD)
-----------------------------------------------
Adds: Drawing augmented reality over camera frames.

DIAGRAM:
(Camera) -> (ADAS Vision System) -> [Detected Object]
      |                                    |
      +------------> (Draw HUD) <----------+
                        |
                        v
              [Frame with Markers]
"""

# pylint: disable=no-member
import random
from typing import Any, Dict, Generator, Tuple
import cv2
import numpy as np
from wpipe import For, Pipeline, step, to_obj


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


@step(name="activate_adas_vision")
@to_obj
def adas_vision(_ctx: Any) -> Dict[str, Any]:
    """Simulate an ADAS vision system.

    Args:
        _ctx (Any): The context object.

    Returns:
        Dict[str, Any]: Vehicle detection and distance.
    """
    # The assistance system detects if there is a car in front
    distance = random.randint(10, 100)
    return {"vehicle_in_front": True, "distance_m": distance}


@step(name="render_hud")
@to_obj
def render_hud(ctx: Any) -> Dict[str, Any]:
    """Simulate an intelligent windshield drawing on the frame.

    Args:
        ctx (Any): The context object.

    Returns:
        Dict[str, Any]: Visualization frame.
    """
    # We simulate the smart windshield by drawing on the frame
    frame_id, frame = next(ctx.stream)
    color = (0, 255, 0) if ctx.distance_m > 30 else (0, 0, 255)

    # Draw info on the 'windshield' (frame)
    cv2.putText(
        frame,
        f"OBJ: CAR | DIST: {ctx.distance_m}m",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2,
    )

    print(f"🖥️  HUD [Frame {frame_id}]: Visualizing vehicle at {ctx.distance_m}m")
    return {"visualization": frame}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L10_HUD", verbose=True)
    pipeline.set_steps(
        [start_camera, For(iterations=3, steps=[adas_vision, render_hud])]
    )
    pipeline.run({})
