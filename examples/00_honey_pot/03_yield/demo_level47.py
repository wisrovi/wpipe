"""
DEMO LEVEL 47: Async with Simulated For Loop
---------------------------------------------
Adds: Loop in async pipeline (simulated with sequential steps).
Continues: L46.

DIAGRAM:
Steps executed 3 times sequentially
"""

import asyncio
from typing import Any
from wpipe import PipelineAsync

async def process_frame_0(data: Any) -> None:
    """Process frame 0 step asynchronously.

    Args:
        data: Input data.
    """
    print("🖼️ [ASYNC] Frame 0")

async def process_frame_1(data: Any) -> None:
    """Process frame 1 step asynchronously.

    Args:
        data: Input data.
    """
    print("🖼️ [ASYNC] Frame 1")

async def process_frame_2(data: Any) -> None:
    """Process frame 2 step asynchronously.

    Args:
        data: Input data.
    """
    print("🖼️ [ASYNC] Frame 2")

async def main() -> None:
    """Main async entry point."""
    pipe = PipelineAsync(pipeline_name="trip_l47_asyncfor", verbose=True)
    pipe.set_steps([process_frame_0, process_frame_1, process_frame_2])
    print("\n>>> Testing async with loop...\n")
    try:
        await pipe.run({})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
