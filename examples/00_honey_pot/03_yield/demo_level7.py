"""
DEMO LEVEL 7: Loops (For)
-------------------------
Adds: Use of For() to process frames repeatedly.

DIAGRAM:
(start_camera) --> [stream: <generator>]
      |
      v
   For(10 iterations) {
      (process_frame) -> Consumes 'next(ctx.stream)'
   }
"""

from typing import Any, Dict, Generator, Tuple
import numpy as np
from wpipe import For, Pipeline, step, to_obj


def simulate_video() -> Generator[Tuple[int, np.ndarray], None, None]:
    """Simulate a video stream.

    Yields:
        Tuple[int, np.ndarray]: Frame ID and image.
    """
    for i in range(10):
        yield i, np.zeros((100, 100, 3), dtype=np.uint8)


@step(name="start_camera")
def start_camera(_data: Dict[str, Any]) -> Dict[str, Any]:
    """Initialize camera stream.

    Args:
        _data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: The stream generator.
    """
    return {"stream": simulate_video()}


@step(name="process_frame")
@to_obj
def process_frame(ctx: Any) -> Dict[str, Any]:
    """Consume the next frame from the stream in a loop.

    Args:
        ctx (Any): The context object.

    Returns:
        Dict[str, Any]: Current frame ID or error if finished.
    """
    # Extract the next frame from the generator stored in the warehouse
    try:
        frame_id, _ = next(ctx.stream)
        print(f"🖼️ Processing frame: {frame_id}")
        return {"current_frame": frame_id}
    except StopIteration:
        return {"error": "Stream finished"}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L7", verbose=True)
    pipeline.set_steps(
        [
            start_camera,
            # Execute the processing step 5 times
            For(iterations=5, steps=[process_frame]),
        ]
    )
    pipeline.run({})
