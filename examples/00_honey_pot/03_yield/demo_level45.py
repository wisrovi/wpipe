"""
DEMO LEVEL 45: Async with Checkpoints
-------------------------------------
Adds: Checkpoints in async pipeline.
Continues: L44.

DIAGRAM:
(async start_motor)
      |
      +-- [Checkpoint: engine_on]
      |
      v
(async drive)
"""

import asyncio
from typing import Any, Dict
from wpipe import PipelineAsync

async def start_motor(data: Any) -> Dict[str, str]:
    """Start motor step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: Engine status.
    """
    await asyncio.sleep(0.05)
    print("🔑 [ASYNC] Motor started")
    return {"engine": "on"}

async def drive(data: Any) -> Dict[str, bool]:
    """Drive step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, bool]: Driving status.
    """
    await asyncio.sleep(0.05)
    print("🚗 [ASYNC] Driving...")
    return {"driving": True}

if __name__ == "__main__":

    async def main() -> None:
        """Main async entry point."""
        pipe = PipelineAsync(pipeline_name="trip_l45_asynccheckpoint", verbose=True)

        pipe.add_checkpoint(
            checkpoint_name="engine_on",
            expression="engine == 'on'",
        )

        pipe.set_steps([start_motor, drive])
        print("\n>>> Testing async with checkpoints...\n")
        try:
            await pipe.run({})
        except Exception as e:
            print(f"Error: {e}")

    asyncio.run(main())
