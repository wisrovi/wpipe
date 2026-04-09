"""
Example demonstrating task timeout functionality.

Shows how to set timeouts on tasks to prevent hanging and ensure
pipeline reliability in production environments.
"""

import time
import asyncio
from wpipe import Pipeline, PipelineAsync, timeout_sync, timeout_async, TaskTimer, TimeoutError


@timeout_sync(seconds=2)
def fast_task(data: dict) -> dict:
    """Task that completes within timeout."""
    print("[Fast Task] Starting (2s timeout)...")
    time.sleep(1)
    print("[Fast Task] ✓ Completed in time")
    return {"fast_task": "completed"}


@timeout_sync(seconds=1)
def hanging_task(data: dict) -> dict:
    """Task that would hang without timeout."""
    print("[Hanging Task] Starting (1s timeout)...")
    try:
        time.sleep(5)  # This will timeout
        return {"hanging_task": "this won't execute"}
    except TimeoutError as e:
        print(f"[Hanging Task] ✗ Timeout: {e}")
        raise


async def async_fast_task(data: dict) -> dict:
    """Async task that completes within timeout."""
    print("[Async Fast Task] Starting (2s timeout)...")
    await asyncio.sleep(1)
    print("[Async Fast Task] ✓ Completed in time")
    return {"async_fast": "completed"}


async def async_timeout_demo():
    """Async task with timeout."""
    print("[Async Slow Task] Starting (1s timeout)...")
    try:
        await timeout_async(1.0, asyncio.sleep(5))
        return {"async_slow": "this won't execute"}
    except TimeoutError as e:
        print(f"[Async Slow Task] ✗ Timeout: {e}")
        raise


def demo_sync_timeouts():
    """Demonstrate synchronous task timeouts."""
    print("\n" + "=" * 60)
    print("SYNC TASK TIMEOUTS DEMO")
    print("=" * 60 + "\n")
    
    pipeline = Pipeline(pipeline_name="sync_timeout_demo", verbose=True)
    pipeline.set_steps([
        (fast_task, "fast_task", "v1.0"),
    ])
    
    try:
        result = pipeline.run({})
        print(f"\n✓ Pipeline succeeded: {result}\n")
    except TimeoutError as e:
        print(f"\n✗ Pipeline timeout: {e}\n")


async def demo_async_timeouts():
    """Demonstrate asynchronous task timeouts."""
    print("\n" + "=" * 60)
    print("ASYNC TASK TIMEOUTS DEMO")
    print("=" * 60 + "\n")
    
    pipeline = PipelineAsync(pipeline_name="async_timeout_demo", verbose=True)
    pipeline.set_steps([
        (async_fast_task, "async_fast", "v1.0"),
    ])
    
    try:
        result = await pipeline.run({})
        print(f"\n✓ Async pipeline succeeded: {result}\n")
    except TimeoutError as e:
        print(f"\n✗ Async pipeline timeout: {e}\n")


def demo_task_timer():
    """Demonstrate task timer context manager."""
    print("\n" + "=" * 60)
    print("TASK TIMER CONTEXT MANAGER DEMO")
    print("=" * 60 + "\n")
    
    with TaskTimer("data_processing", timeout_seconds=3) as timer:
        print("[Data Processing] Starting...")
        time.sleep(1.5)
        print("[Data Processing] Halfway done...")
        time.sleep(1)
        print("[Data Processing] Completed!")
    
    print(f"\n✓ Task completed in {timer.elapsed_seconds:.2f}s")
    print(f"  Exceeded timeout? {timer.exceeded_timeout()}\n")


if __name__ == "__main__":
    # Run sync timeout demo
    demo_sync_timeouts()
    
    # Run async timeout demo
    print("\nRunning async demo...")
    asyncio.run(demo_async_timeouts())
    
    # Run task timer demo
    demo_task_timer()
