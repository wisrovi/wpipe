"""
DEMO LEVEL 13: High-Performance CPU (Processes)
-----------------------------------------------
Adds: Use of real cores to process heavy depth maps.
Accumulates: 360° Vision (L12).

DIAGRAM:
[CPU Process 1] -> (Analyze Road Textures)
[CPU Process 2] -> (Recognize Traffic Signs)
[CPU Process 3] -> (Predict Pedestrian Trajectories)
"""

import os
import time
from typing import Any, Dict

from wpipe import Parallel, Pipeline, step

@step(name="deep_analysis")
def deep_analysis(data: Any) -> Dict[str, str]:
    """Deep analysis step simulating heavy AI processing.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Depth map status.
    """
    # Simulate real CPU load of a neural network model
    time.sleep(0.2)
    return {"map": "complete"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l13_heavyai", verbose=True)
    pipe.set_steps(
        [
            Parallel(
                steps=[deep_analysis] * 3,
                max_workers=3,
                use_processes=True,  # <--- Use real AI engine power
            )
        ]
    )
    pipe.run({})
