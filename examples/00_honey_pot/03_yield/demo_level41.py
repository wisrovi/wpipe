"""
DEMO LEVEL 41: Basic Async Pipeline
------------------------------------
Adds: PipelineAsync for asynchronous execution.
Accumulates: Basic pipeline from L1.

DIAGRAM:
(async start_motor) --> [motor: 'ON']
      |
      v
(async verify_sensors) --> [sensors: 'OK']
"""

import asyncio
from typing import Any, Dict
from wpipe import PipelineAsync

def start_motor(data: Any) -> Dict[str, Any]:
    """Start motor step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, Any]: Motor status and fuel level.
    """
    print("🔑 [ASYNC] Motor started")
    return {"motor": "ON", "fuel": 100}

def verify_sensors(data: Any) -> Dict[str, str]:
    """Verify sensors step.

    Args:
        data: Input data for the step.

    Returns:
        Dict[str, str]: Sensors status.
    """
    print("📡 [ASYNC] Sensors verified")
    return {"sensors": "OK"}

if __name__ == "__main__":

    async def main() -> None:
        """Main async entry point."""
        pipe = PipelineAsync(pipeline_name="trip_l41_asyncbasic", verbose=True)
        pipe.set_steps([start_motor, verify_sensors])
        print("\n>>> Starting asynchronous pipeline...\n")
        await pipe.run({})

    asyncio.run(main())
