"""
DEMO LEVEL 8: Branching (Condition)
-----------------------------------
Adds: Use of Condition() to execute True/False branches.

DIAGRAM:
(process_frame)
      |
      v
Condition(Obstacle detected?)
      |--- [True]  -> (emergency_brake)
      |--- [False] -> (gentle_accelerate)
"""

import random
from typing import Any, Dict, Generator, Tuple
import numpy as np
from wpipe import Condition, For, Pipeline, step, to_obj


def simulate_video() -> Generator[Tuple[int, np.ndarray], None, None]:
    """Simulate a video stream.

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
        Dict[str, Any]: Stream generator.
    """
    return {"stream": simulate_video()}


@step(name="process_frame")
@to_obj
def process_frame(ctx: Any) -> Dict[str, Any]:
    """Process a frame and detect hazards.

    Args:
        ctx (Any): The context object.

    Returns:
        Dict[str, Any]: Frame ID and obstacle status.
    """
    try:
        frame_id, _ = next(ctx.stream)
        danger = random.random() < 0.3
        print(f"🖼️ Frame {frame_id} | Danger: {danger}")
        return {"current_frame": frame_id, "obstacle": danger}
    except StopIteration:
        return {"error": "End"}


@step(name="brake")
def brake(data: Dict[str, Any]) -> Dict[str, Any]:
    """Apply emergency brakes.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Action performed.
    """
    print(f"🛑 EMERGENCY BRAKE ACTIVATED! Data: {data}")
    return {"action": "Braking"}


@step(name="accelerate")
def accelerate(data: Dict[str, Any]) -> Dict[str, Any]:
    """Accelerate smoothly.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Action performed.
    """
    print(f"🛣️ Clear road. Accelerating... Data: {data}")
    return {"action": "Accelerating"}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L8", verbose=True)
    pipeline.set_steps(
        [
            start_camera,
            For(
                iterations=5,
                steps=[
                    process_frame,
                    Condition(
                        expression="obstacle == True",
                        branch_true=[brake],
                        branch_false=[accelerate],
                    ),
                ],
            ),
        ]
    )
    pipeline.run({})
