"""
DEMO LEVEL 25: Super-Computer (Multi-Core Benchmark)
----------------------------------------------------
Adds: Real difference between Threads and Processes in Parallel.
Accumulates: Parallelism (L12 and L13).

DIAGRAM:
Parallel(4 heavy vision tasks)
  |-- THREADS   -> ~1.2s (Share CPU)
  |-- PROCESSES -> ~0.3s (Use all cores)
"""

import time
from typing import Any, Dict

from wpipe import Parallel, Pipeline, step

@step(name="deep_vision")
def deep_vision(data: Any) -> Dict[str, str]:
    """Deep vision step with intense CPU load.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: AI status.
    """
    # Real CPU load (intense math)
    start = time.time()
    while time.time() - start < 0.3:
        _ = 100 * 100
    return {"ai": "done"}

if __name__ == "__main__":
    # 1. Threads Mode
    p1 = Pipeline(pipeline_name="eco_mode_threads")
    p1.set_steps(
        [Parallel(steps=[deep_vision] * 4, max_workers=4, use_processes=False)]
    )

    print(">>> [TEST 1] Processing with THREADS (Sharing resources)...")
    t1 = time.time()
    p1.run({})
    print(f"⏱️ Threads Time: {time.time() - t1:.2f}s\n")

    # 2. Processes Mode (NEW L25)
    # Note: when using use_processes=True, ensure context data is serializable
    p2 = Pipeline(pipeline_name="sport_mode_processes")
    p2.set_steps(
        [Parallel(steps=[deep_vision] * 4, max_workers=4, use_processes=True)]
    )

    print(">>> [TEST 2] Processing with PROCESSES (Total Power)...")
    t2 = time.time()
    p2.run({})
    print(f"⏱️ Processes Time: {time.time() - t2:.2f}s")
