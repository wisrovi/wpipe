"""
DEMO LEVEL 20: Emergency Decisions (Condition)
----------------------------------------------
Adds: Dynamic decisions based on AI and speed.
Accumulates: Inference (L10) and Telemetry (L16).

DIAGRAM:
(Vision_System) -> [Obstacle detected]
      |
      v
Condition(Emergency braking?)
      |--- [YES] -> (Activate ABS Brakes)
      |--- [NO] -> (Maintain Speed)
"""
from typing import Any, Dict
from wpipe import Pipeline, step, Condition

@step(name="ai_radar")
def ai_radar(data: Any) -> Dict[str, Any]:
    """AI Radar detection step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, Any]: Distance and obstacle presence.
    """
    # Simulate obstacle detection at 5 meters
    return {"distance": 5, "obstacle": True}

@step(name="abs_braking")
def abs_braking(data: Any) -> Dict[str, bool]:
    """ABS braking step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Braking status.
    """
    print("🚨 ABS: Braking sharply to avoid collision!")
    return {"braking": True}

@step(name="maintain_speed")
def maintain_speed(data: Any) -> Dict[str, bool]:
    """Maintain speed step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Braking status.
    """
    print("🛣️  Everything clear. Maintaining cruise speed.")
    return {"braking": False}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l20_emergencylogic", verbose=True)

    pipe.set_steps([
        ai_radar,
        # NEW IN L20: The car decides which branch to execute
        Condition(
            expression="obstacle == True and distance < 10",
            branch_true=[abs_braking],
            branch_false=[maintain_speed]
        )
    ])

    pipe.run({})
