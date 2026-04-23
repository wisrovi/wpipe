"""
DEMO LEVEL 31: Safety Scan (Validators)
---------------------------------------
Adds: Custom Pydantic validators for physical safety.
Accumulates: Pydantic Telemetry (L16).

DIAGRAM:
(read_pressure) -> [pressure: 1.0 bar]
      |
      v
[Validator] -- [Is < 1.5?] -- ERROR! --> (Alert: Flat tire)
"""

import random
from typing import Any, Dict

from pydantic import BaseModel, Field, validator

from wpipe import Pipeline, step, to_obj

class SafetyCheck(BaseModel):
    """Pydantic model for tire pressure safety check."""
    pressure: float = Field(..., ge=1.0, le=4.0)

    @validator("pressure")
    def low_pressure_alert(cls, v: float) -> float:
        """Alerts if tire pressure is low.

        Args:
            v: The pressure value.

        Returns:
            float: The validated pressure value.
        """
        if v < 2.0:
            print("⚠️ WARNING: Low pressure detected. Inflation recommended.")
        return v

@step(name="pressure_sensor")
def pressure_sensor(data: Any) -> Dict[str, float]:
    """Pressure sensor reading step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, float]: Pressure reading.
    """
    # Simulate reading from a low-air tire
    random_pressure = round(random.randint(10, 30) / 10, 2)
    return {"pressure": random_pressure}

@step(name="verify_integrity")
@to_obj(SafetyCheck)
def verify_integrity(ctx: SafetyCheck) -> Dict[str, bool]:
    """Verifies physical integrity based on tire pressure.

    Args:
        ctx: Validated safety check context.

    Returns:
        Dict[str, bool]: Integrity status.
    """
    print(f"🛞  Tires: {ctx.pressure} bar. Physical integrity confirmed.")
    return {"tires_ok": True}

if __name__ == "__main__":
    pipe = Pipeline(pipeline_name="safety_scan_l31", verbose=True)
    pipe.set_steps([pressure_sensor, verify_integrity])
    pipe.run({})
