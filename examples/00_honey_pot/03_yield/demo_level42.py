"""
DEMO LEVEL 42: Step Decorator Async
-----------------------------------
Adds: Async functions within the pipeline.
Continues: L41.

DIAGRAM:
(async verify_battery) --> [battery: 85%]
       |
       v
(async start_system) --> [system: 'ON']
"""

import asyncio
from typing import Any, Dict
from wpipe import PipelineAsync

async def verify_battery(data: Any) -> Dict[str, int]:
    """Verify battery step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, int]: Battery level.
    """
    await asyncio.sleep(0.05)
    print("🔋 [ASYNC] Battery at 85%")
    return {"battery": 85}

async def start_system(data: Any) -> Dict[str, str]:
    """Start system step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: System status.
    """
    await asyncio.sleep(0.05)
    print("🟢 [ASYNC] System started")
    return {"system": "ON"}

if __name__ == "__main__":

    async def main() -> None:
        """Main async entry point."""
        pipe = PipelineAsync(pipeline_name="trip_l42_asyncstep", verbose=True)
        pipe.set_steps([verify_battery, start_system])
        print("\n>>> Testing async functions...\n")
        await pipe.run({})

    asyncio.run(main())
