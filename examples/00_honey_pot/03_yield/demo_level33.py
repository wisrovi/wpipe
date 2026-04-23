"""
DEMO LEVEL 33: 360° Vision Fusion (Deltas)
------------------------------------------
Adds: Process parallelism that adds data without colliding.
Accumulates: Multiprocess (L13) and Delta Merging (Library).

DIAGRAM:
Parallel(PROCESSES)
  [CPU 1] -> (AI_Signals) -> Adds 'signals'
  [CPU 2] -> (AI_Objects) -> Adds 'objects'
      |
      v
[Final Context] -> Possesses BOTH results (Intelligent fusion).
"""

from typing import Any, Dict, List
from wpipe import Parallel, Pipeline, step

@step(name="ai_signals")
def ai_signals(data: Any) -> Dict[str, List[str]]:
    """AI Traffic signal analysis step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, List[str]]: Detected traffic signals.
    """
    print("🛑 CPU-1: Analyzing traffic signals...")
    return {"signals": ["Stop", "60km/h"]}

@step(name="ai_objects")
def ai_objects(data: Any) -> Dict[str, List[str]]:
    """AI Pedestrian and obstacle analysis step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, List[str]]: Detected objects.
    """
    print("🚶 CPU-2: Analyzing pedestrians and obstacles...")
    return {"objects": ["Pedestrian crossing"]}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="vision_360_l33", verbose=True)
    pipe.set_steps(
        [Parallel(steps=[ai_signals, ai_objects], max_workers=2, use_processes=True)]
    )

    final_results = pipe.run({})
    print(f"\n📊 FULL 360 MAP: {list(final_results.keys())}")
    print(f"   Detections: {final_results.get('signals')} + {final_results.get('objects')}")
