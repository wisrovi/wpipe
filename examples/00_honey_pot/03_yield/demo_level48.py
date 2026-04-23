"""
DEMO LEVEL 48: Async with Metrics
---------------------------------
Adds: Metrics in async pipeline.
Continues: L47.

DIAGRAM:
(async process_data) --> [Metric: processed_data]
"""

import asyncio
from typing import Any, Dict
from wpipe import PipelineAsync, Metric

async def process_data(data: Any) -> Dict[str, int]:
    """Process data step asynchronously and record metrics.

    Args:
        data: Input data.

    Returns:
        Dict[str, int]: Processed amount.
    """
    await asyncio.sleep(0.05)
    print("📊 [ASYNC] Processing data...")
    Metric.record("processed_data", 100)
    return {"processed": 100}

async def main() -> None:
    """Main async entry point."""
    pipe = PipelineAsync(pipeline_name="trip_l48_asyncmetric", verbose=True)
    pipe.set_steps([process_data])
    print("\n>>> Testing async with metrics...\n")
    try:
        await pipe.run({})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
