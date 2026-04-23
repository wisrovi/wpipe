"""
DEMO LEVEL 28: The Driver's Diary (Events)
------------------------------------------
Adds: Manual markers on the timeline.
Accumulates: Metrics and Tracking.

DIAGRAM:
[Trip] ---- [Event: 'Radar Detected'] ---- [Trip] ---- [Event: 'Coffee Break']
"""

from typing import Any, Dict
from wpipe import Pipeline, step

@step(name="cross_border")
def cross_border(data: Any) -> Dict[str, str]:
    """Cross border step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Country status.
    """
    print("🌍 Crossing border: Changing traffic regulations...")
    return {"country": "Portugal"}

if __name__ == "__main__":
    pipe = Pipeline(
        pipeline_name="travel_log_l28",
        tracking_db="output/car_events.db",
        verbose=True,
    )

    # NEW IN L28: Note milestones that don't change the context but are recorded
    pipe.add_event(
        event_type="annotation",
        event_name="Route Start",
        message="Driver: William R. | Weather: Clear",
    )

    pipe.set_steps([cross_border])
    pipe.run({})
