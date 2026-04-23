"""
DEMO LEVEL 44: Async Parallel
-----------------------------
Adds: Parallel async steps.
Continues: L43.

DIAGRAM:
Parallel(async steps) {
  |-- (async front_camera)
  |-- (async rear_camera)
  |-- (async radar)
}
"""

import asyncio
from typing import Any, Dict
from wpipe import PipelineAsync, Parallel

async def front_camera(data: Any) -> Dict[str, str]:
    """Front camera activation step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: Camera status.
    """
    await asyncio.sleep(0.05)
    print("📷 [ASYNC] Front camera activated")
    return {"front": "active"}

async def rear_camera(data: Any) -> Dict[str, str]:
    """Rear camera activation step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: Camera status.
    """
    await asyncio.sleep(0.05)
    print("📷 [ASYNC] Rear camera activated")
    return {"rear": "active"}

async def radar(data: Any) -> Dict[str, str]:
    """Radar activation step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: Radar status.
    """
    await asyncio.sleep(0.05)
    print("📡 [ASYNC] Radar activated")
    return {"radar": "active"}

async def main() -> None:
    """Main async entry point."""
    pipe = PipelineAsync(pipeline_name="trip_l44_asyncparallel", verbose=True)
    pipe.set_steps(
        [Parallel(steps=[front_camera, rear_camera, radar], max_workers=3)]
    )
    print("\n>>> Testing async parallel...\n")
    await pipe.run({})

if __name__ == "__main__":
    asyncio.run(main())
