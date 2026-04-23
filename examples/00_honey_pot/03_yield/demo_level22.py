"""
DEMO LEVEL 22: Signal Recovery (Retries)
----------------------------------------
Adds: retry_count and retry_delay for intermittent failures.
Accumulates: Telemetry (L16).

DIAGRAM:
(connect_gps) -- [Fail] -> Wait 0.5s -> Retry 1
      |--- [Fail] -> Wait 0.5s -> Retry 2
      |--- [Connected!] -> Continue route.
"""

import random
from typing import Any, Dict

from wpipe import Pipeline, step


# NEW IN L22: Retries up to 10 times before giving up
@step(name="connect_gps", retry_count=2, retry_delay=0.5)
def connect_gps(data: Any) -> Dict[str, float]:
    """Connect to GPS step with retries.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, float]: GPS coordinates.

    Raises:
        ConnectionError: If signal is weak.
    """
    if random.random() < 0.8:  # Simulate poor coverage under a bridge
        print("🛰️ GPS: Searching for satellite signal...")
        raise ConnectionError("Weak signal")

    print("🛰️ GPS: Position fixed successfully!")
    return {"lat": 40.41, "lon": -3.70}


if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l22_gps_recovery", verbose=True)
    pipe.set_steps([connect_gps])

    print(
        ">>> Starting navigation: The system will recover on its own from signal losses."
    )
    try:
        pipe.run({})
    except ConnectionError as e:
        print("ConnectionError", e)
    except Exception as e:
        print("Exception", e)
