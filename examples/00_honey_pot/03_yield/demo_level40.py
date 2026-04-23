"""
DEMO LEVEL 40: THE GRAND FINALE (Total Autonomy)
------------------------------------------------
Summary: Integration of the 40 functionalities in a real trip.
Accumulates: ABSOLUTELY EVERYTHING.

FINAL DIAGRAM:
[Start] -> (Load YAML) -> (Checkpoints) -> For(Route) {
   Parallel(Multiprocess AI) -> Condition(Obstacle) -> Pydantic(Validate) -> Metric(Fuel)
} -> [Destination] -> (Shutdown Hooks) -> (Export CSV)
"""

import os
import random
from typing import Any, Dict

from pydantic import BaseModel, Field

from wpipe import (
    CheckpointManager,
    Condition,
    For,
    Metric,
    Parallel,
    Pipeline,
    PipelineExporter,
    step,
    to_obj,
)

# 1. Secure Data Definition
class CarStatus(BaseModel):
    """Pydantic model for vehicle status validation."""
    fuel: float = Field(..., ge=0, le=100)
    speed: float = Field(..., ge=0, le=200)

# 2. Vision Intelligence
@step(name="ai_vision_360")
def ai_vision_360(data: Any) -> Dict[str, Any]:
    """AI Vision 360 processing step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, Any]: Detection status and distance.
    """
    danger = random.random() < 0.2
    return {"obstacle": danger, "distance": random.randint(2, 50)}

# 3. Automatic Response
@step(name="emergency_braking")
def emergency_braking(data: Any) -> Dict[str, bool]:
    """Emergency braking step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, bool]: Braking status.
    """
    print("🚨 ADAS: EMERGENCY BRAKING ACTIVATED!")
    return {"braking": True}

# Validation and Metrics
@to_obj(CarStatus)
def validate_telemetry(ctx: CarStatus) -> Dict[str, bool]:
    """Validates telemetry and records speed metric.

    Args:
        ctx: Validated CarStatus context.

    Returns:
        Dict[str, bool]: Validation status.
    """
    Metric.record("trip_speed", ctx.speed, "km/h")
    return {"v_ok": True}

if __name__ == "__main__":
    # Infrastructure preparation
    os.makedirs("output", exist_ok=True)
    TRACKING_DB = "output/grand_trip_2026.db"
    CK_MGR = CheckpointManager("output/trip_control_points.db")

    # THE SUPER PIPELINE: Configured with the full arsenal
    trip = Pipeline(
        pipeline_name="total_autonomous_trip",
        tracking_db=TRACKING_DB,
        collect_system_metrics=True,
        continue_on_error=True,
        verbose=True,
    )

    # Master flow definition
    trip.set_steps(
        [
            # Start and Preparation
            (lambda d: {"fuel": 100, "speed": 120}, "initial_start", "v1.0"),
            # Main Driving Loop
            For(
                iterations=3,
                steps=[
                    # Look in parallel using multiple cores (Multiprocess)
                    Parallel(steps=[ai_vision_360] * 3, use_processes=True, max_workers=3),
                    # Logical decision
                    Condition(expression="obstacle == True", branch_true=[emergency_braking]),
                    validate_telemetry,
                ],
            ),
            (
                lambda d: print("🏁 DESTINATION REACHED: The car has arrived on its own."),
                "finish",
                "v1.0",
            ),
        ]
    )

    # Event and Hook Registration
    trip.add_event(
        event_type="log", event_name="Departure", message="Starting Madrid-Valencia route"
    )
    trip.add_event(
        event_type="hook",
        event_name="Final Protocol",
        steps=[(lambda d: print("🔌 Systems disconnected."), "shutdown", "v1.0")],
    )

    # MASTER EXECUTION
    print("\n🚀 STARTING THE GRAND TRIP (Integration of 40 levels)...\n")
    trip.run({}, checkpoint_mgr=CK_MGR, checkpoint_id="final_autonomous_trip")

    # Exporting the final report for the owner
    PipelineExporter(TRACKING_DB).export_pipeline_logs(
        "output/owner_report.csv", export_format="csv"
    )
    print("\n✅ LEARNING TOUR COMPLETED. 40 LEVELS OF WPIPE MASTERY.")
