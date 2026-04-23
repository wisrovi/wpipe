"""
DEMO LEVEL 16: Secure Telemetry (Pydantic)
------------------------------------------
Adds: Validation of sensor data with Pydantic models.
Accumulates: Vehicle telemetry (L3).

DIAGRAM:
(read_sensors) -> [pressure: 2.2, fuel: 80]
      |
      v
(validate_telemetry @to_obj(Model)) -> Ensures real physical data!
"""

import random
from typing import Any, Dict

from pydantic import BaseModel, Field

from wpipe import Pipeline, step, to_obj

# NEW IN L16: The car only accepts data in logical physical ranges
class SensorData(BaseModel):
    """Pydantic model for sensor data validation."""
    tire_pressure: float = Field(..., ge=1.5, le=3.5)
    fuel_level: float = Field(..., ge=0, le=100)

@step(name="read_obd2")
def read_obd2(data: Any) -> Dict[str, Any]:
    """Read OBD2 data step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, Any]: Sensor readings.
    """
    print("📡 Reading OBD2 data bus...")

    if random.random() < 0.5:
        # This will fail validation because fuel_level is missing
        return {"tire_pressure": 2.3, "brake_activated": True}

    return {"tire_pressure": 2.3, "fuel_level": 75.0}

@step(name="analyze_safety")
@to_obj(SensorData)  # <--- ACTIVE VALIDATION
def analyze_safety(ctx: SensorData) -> Dict[str, bool]:
    """Analyzes vehicle safety based on validated telemetry.

    Args:
        ctx: Validated sensor data context.

    Returns:
        Dict[str, bool]: Safety status.
    """
    print(
        f"📊 Validated Telemetry: Pressure={ctx.tire_pressure}bar, Fuel={ctx.fuel_level}%"
    )
    return {"safe_to_circulate": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="trip_l16_securedata", verbose=True)
    pipe.set_steps([read_obd2, analyze_safety])

    try:
        pipe.run({})
    except Exception as e:
        print(f"Validation Error: {e}")
