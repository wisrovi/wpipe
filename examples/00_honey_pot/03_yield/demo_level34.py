"""
DEMO LEVEL 34: Fault Isolation (Continue on Error)
--------------------------------------------------
Adds: continue_on_error=True for secondary systems.
Accumulates: Error Management (L11).

DIAGRAM:
(Safety_Braking) -> OK
      |
(Radio_Spotify)   -> ERROR! (No internet)
      |
(Cruise_Control)  -> STILL WORKING!
"""

from typing import Any, Dict
from wpipe import Pipeline, step

@step(name="piloting_system")
def piloting_system(data: Any) -> Dict[str, str]:
    """Main piloting system step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Piloting status.
    """
    return {"piloting": "ACTIVE"}

@step(name="infotainment")
def infotainment(data: Any) -> None:
    """Infotainment system step with potential failure.

    Args:
        data: Input data for the step.

    Raises:
        RuntimeError: If network error occurs.
    """
    print("🎵 Radio: Trying to connect to the cloud...")
    raise RuntimeError("Network error: Streaming not available")

@step(name="maintain_distance")
def maintain_distance(data: Any) -> Dict[str, bool]:
    """Radar distance maintenance step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Distance status.
    """
    print("📏 Radar: Maintaining active safety distance.")
    return {"distance_ok": True}

if __name__ == "__main__":
    # NEW IN L34: A radio error does not stop navigation
    pipe = Pipeline(
        pipeline_name="isolation_system_l34", continue_on_error=True, verbose=True
    )

    pipe.set_steps([piloting_system, infotainment, maintain_distance])

    print(">>> Starting trip: Secondary failures will not affect driving.")
    pipe.run({})
