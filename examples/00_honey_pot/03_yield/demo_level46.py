"""
DEMO LEVEL 46: Async with Condition
-----------------------------------
Adds: Condition in async pipeline.
Continues: L45.

DIAGRAM:
(async evaluate_situation)
      |
      +-- (obstacle == True) -> [BRAKE]
      +-- (obstacle == False) -> [ACCELERATE]
"""

import asyncio
import random
from typing import Any, Dict
from wpipe import PipelineAsync, Condition

async def evaluate_situation(data: Any) -> Dict[str, bool]:
    """Evaluate situation step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, bool]: Obstacle presence.
    """
    await asyncio.sleep(0.05)
    obstacle = random.random() < 0.3
    print(f"🚗 [ASYNC] Evaluation: obstacle={obstacle}")
    return {"obstacle": obstacle}

async def brake(data: Any) -> Dict[str, str]:
    """Brake step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: Action performed.
    """
    print("🛑 [ASYNC] Emergency braking")
    return {"action": "brake"}

async def accelerate(data: Any) -> Dict[str, str]:
    """Accelerate step asynchronously.

    Args:
        data: Input data.

    Returns:
        Dict[str, str]: Action performed.
    """
    print("🚀 [ASYNC] Accelerating")
    return {"action": "accelerate"}

async def main() -> None:
    """Main async entry point."""
    pipe = PipelineAsync(pipeline_name="trip_l46_asynccondition", verbose=True)
    pipe.set_steps(
        [
            evaluate_situation,
            Condition(
                expression="obstacle == True",
                branch_true=[brake],
                branch_false=[accelerate],
            ),
        ]
    )
    print("\n>>> Testing async with conditions...\n")
    try:
        await pipe.run({})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
