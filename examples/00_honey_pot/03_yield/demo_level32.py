"""
DEMO LEVEL 32: The Resilience Tunnel (Retries)
-----------------------------------------------
Adds: Retries with prolonged wait for persistent failures.
Accumulates: Retries (L22).

DIAGRAM:
(connect_gps) -- [Fail 1] -> Wait 0.5s
      |--- [Fail 2] -> Wait 0.5s
      |--- [Fail 3] -> Wait 0.5s (Leaving the tunnel...)
      |--- [SUCCESS!] -> Signal recovered.
"""

from typing import Any, Dict
from wpipe import Pipeline, step

# Global counter to simulate retry success after some attempts
RETRY_ATTEMPT = 0

@step(name="recover_gps", retry_count=3, retry_delay=0.5)
def recover_gps(data: Any) -> Dict[str, bool]:
    """Recover GPS signal step with retries.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Signal lock status.

    Raises:
        ConnectionError: If signal is not locked.
    """
    global RETRY_ATTEMPT
    RETRY_ATTEMPT += 1
    if RETRY_ATTEMPT < 3:
        print(f"📡 Satellite: Attempt {RETRY_ATTEMPT} failed (Tunnel)...")
        raise ConnectionError("No visibility")

    print("📡 Satellite: GPS signal fixed!")
    return {"locked": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="gps_tunnel_l32", verbose=True)
    pipe.set_steps([recover_gps])
    print(">>> Entering low coverage zone (Tunnel)...")
    pipe.run({})
