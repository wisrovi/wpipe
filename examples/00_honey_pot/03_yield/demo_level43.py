"""
DEMO LEVEL 43: Async with Retry (Using Pipeline)
-----------------------------------------------
Adds: Retry in async pipeline.
Continues: L42.

DIAGRAM:
(connect_car) -[fail]-> retry --> [connected]
"""

import asyncio
import random
from typing import Any, Dict
from wpipe import PipelineAsync

async def connect_car(data: Any) -> Dict[str, bool]:
    """Connect car step asynchronously with potential failure.

    Args:
        data: Input data.

    Returns:
        Dict[str, bool]: Connection status.

    Raises:
        ConnectionError: If Bluetooth is unavailable.
    """
    if random.random() < 0.4:
        raise ConnectionError("Bluetooth unavailable")
    print("📱 [ASYNC] Car connected")
    return {"connected": True}

async def sync_data(data: Any) -> Dict[str, str]:
    """Synchronize data step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: Sync status.
    """
    print("🔄 [ASYNC] Data synchronized")
    return {"sync": "ok"}

if __name__ == "__main__":

    async def main() -> None:
        """Main async entry point."""
        pipe = PipelineAsync(
            pipeline_name="trip_l43_asyncretry",
            verbose=True,
            max_retries=3,
            retry_delay=0.1,
        )
        pipe.set_steps([connect_car, sync_data])
        print("\n>>> Testing async retry...\n")
        try:
            await pipe.run({})
        except ConnectionError as e:
            print(f"Error: {e}")

    asyncio.run(main())
