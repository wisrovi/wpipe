"""
DEMO LEVEL 23: Compartmentalization (Data Filtering)
----------------------------------------------------
Adds: Passing sub-contexts to protect sensitive data.
Accumulates: Modularization (L19).

DIAGRAM:
[Global Context: engine_id, position, image, speed]
      |
      v
(Ads_AI) <- Only receives 'position'! (Privacy)
"""

from typing import Any, Dict
from wpipe import Pipeline, step

@step(name="full_telemetry")
def full_telemetry(data: Any) -> Dict[str, Any]:
    """Full telemetry gathering step.

    Args:
        data: Input data.

    Returns:
        Dict[str, Any]: Engine ID, position, and speed.
    """
    return {"engine_id": "X-100", "position": "Gran Via", "speed": 50}

# NEW IN L23: A step that only sees what we filter for it
@step(name="suggest_restaurants")
def suggest_restaurants(data: Dict[str, Any]) -> Dict[str, str]:
    """Restaurant suggestion step based on filtered position.

    Args:
        data: Filtered input data.

    Returns:
        Dict[str, str]: Suggestion details.
    """
    # Verify we cannot see 'engine_id'
    id_visible = "engine_id" in data
    print(
        f"📍 Suggestion in {data.get('position')}: Engine ID visible? {id_visible}"
    )
    return {"suggestion": "VIPS 200m away"}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l23_privacy", verbose=True)

    pipe.set_steps(
        [
            full_telemetry,
            # Filter the context using an intermediate lambda
            (lambda d: {"position": d["position"]}, "PrivacyFilter", "v1.0"),
            suggest_restaurants,
        ]
    )

    pipe.run({})
