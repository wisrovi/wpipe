"""
Basic async timeout example.

Demonstrates timeout handling for async functions.
"""

import asyncio
from wpipe import timeout_async, TimeoutError

async def quick_async_task():
    """Async task that completes within timeout."""
    print("Starting quick async task...")
    await asyncio.sleep(1)
    print("Quick async task completed!")
    return {"result": "success", "time": 1}

async def slow_async_task():
    """Async task that exceeds timeout."""
    print("Starting slow async task...")
    await asyncio.sleep(5)  # This will timeout
    return {"result": "success"}

async def demo_async_timeouts():
    """Demonstrate async timeout handling."""
    
    # Example 1: Task that completes
    print("--- Example 1: Quick Async Task ---")
    try:
        result = await timeout_async(3, quick_async_task())
        print(f"Result: {result}\n")
    except TimeoutError as e:
        print(f"✗ Timeout: {e}\n")
    
    # Example 2: Task that exceeds timeout
    print("--- Example 2: Slow Async Task ---")
    try:
        result = await timeout_async(2, slow_async_task())
        print(f"Result: {result}\n")
    except TimeoutError as e:
        print(f"✗ Timeout occurred: {e}\n")
    
    # Example 3: Multiple concurrent tasks with timeout
    print("--- Example 3: Concurrent Tasks ---")
    tasks = [
        timeout_async(2, quick_async_task()),
        timeout_async(2, quick_async_task()),
        timeout_async(1, asyncio.sleep(2)),  # This one will timeout
    ]
    
    results = []
    for task in tasks:
        try:
            result = await task
            results.append(("success", result))
        except TimeoutError:
            results.append(("timeout", None))
        except Exception as e:
            results.append(("error", str(e)))
    
    print(f"Results: {len([r for r in results if r[0] == 'success'])} successful, "
          f"{len([r for r in results if r[0] == 'timeout'])} timed out")

if __name__ == "__main__":
    print("=== Basic Async Timeout Example ===\n")
    asyncio.run(demo_async_timeouts())
