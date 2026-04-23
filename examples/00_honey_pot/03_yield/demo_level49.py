"""
DEMO LEVEL 49: Async Tracking
-----------------------------
Adds: Tracking in async pipeline.
Continues: L48.

DIAGRAM:
(async start_motor) --> [tracked]
"""

import asyncio
from typing import Any, Dict
from wpipe import PipelineAsync

async def start_motor(data: Any) -> Dict[str, str]:
    """Start motor step asynchronously with tracking enabled.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: Motor status.
    """
    await asyncio.sleep(0.05)
    print("🔑 [ASYNC] Motor started and tracked")
    return {"motor": "on"}

async def main() -> None:
    """Main async entry point."""
    db_path = "output/async_tracking.db"
    pipe = PipelineAsync(
        pipeline_name="trip_l49_asynctracking",
        verbose=True,
        tracking_db=db_path,
    )
    pipe.set_steps([start_motor])
    print("\n>>> Testing async with tracking...\n")
    result = await pipe.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
