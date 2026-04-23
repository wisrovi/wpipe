"""
DEMO LEVEL 6: Generators (Data Stream)
--------------------------------------
Adds: Use of generators (yield) to simulate a camera stream.

DIAGRAM:
[Initial Configuration]
      |
      v
(Prepare Car) -> [engine, gps, climate]
      |
      v
(start_camera) -> Returns a Generator (yield)
      |
      v
[Warehouse with 'stream': <generator object>]
"""

from typing import Any, Dict, Generator, Tuple
import numpy as np
from wpipe import Pipeline, step


def prepare_car(_data: Dict[str, Any]) -> Dict[str, Any]:
    """Prepare the car for the trip.

    Args:
        _data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: Engine and GPS status.
    """
    return {"engine": "ON", "gps": "Valencia"}


def simulate_video() -> Generator[Tuple[int, np.ndarray], None, None]:
    """Simulate a video stream using a generator.

    Yields:
        Tuple[int, np.ndarray]: Frame ID and a black image.
    """
    for i in range(10):
        # Simulate a black image with the frame ID
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        yield i, img


@step(name="start_camera")
def start_camera(data: Dict[str, Any]) -> Dict[str, Any]:
    """Activate the camera and store the stream in the warehouse.

    Args:
        data (Dict[str, Any]): The current pipeline context data.

    Returns:
        Dict[str, Any]: The video stream generator.
    """
    print(f"📸 Front camera: Activated. Input data: {data}")
    # The generator is stored in the warehouse to be consumed later
    return {"stream": simulate_video()}


if __name__ == "__main__":
    pipeline = Pipeline(pipeline_name="Trip_L6", verbose=True)
    pipeline.set_steps([prepare_car, start_camera])
    pipeline.run({})
