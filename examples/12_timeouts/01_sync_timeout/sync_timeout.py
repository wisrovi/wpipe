"""
Basic synchronous timeout example.

Demonstrates timeout handling for sync functions.
"""

from wpipe import timeout_sync, TaskTimer, TimeoutError
import time

@timeout_sync(seconds=2)
def quick_task():
    """Task that completes within timeout."""
    print("Starting quick task...")
    time.sleep(1)
    print("Quick task completed!")
    return {"result": "success"}

@timeout_sync(seconds=2)
def slow_task():
    """Task that exceeds timeout."""
    print("Starting slow task...")
    time.sleep(5)  # This will timeout
    return {"result": "success"}

def manual_timeout_example():
    """Example using TaskTimer with manual timeout checking."""
    print("\n--- Manual Timeout Example ---")
    
    with TaskTimer("manual_task", timeout_seconds=3) as timer:
        print("Starting work...")
        time.sleep(2)
        print(f"Work completed in {timer.elapsed_seconds:.2f}s")
        
        if timer.exceeded_timeout():
            print("⚠ Work exceeded timeout!")
        else:
            print("✓ Work completed within timeout")

if __name__ == "__main__":
    print("=== Basic Sync Timeout Example ===\n")
    
    # Example 1: Task that completes
    print("--- Example 1: Quick Task ---")
    try:
        result = quick_task()
        print(f"Result: {result}\n")
    except TimeoutError as e:
        print(f"✗ Timeout: {e}\n")
    
    # Example 2: Task that exceeds timeout
    print("--- Example 2: Slow Task ---")
    try:
        result = slow_task()
        print(f"Result: {result}\n")
    except TimeoutError as e:
        print(f"✗ Timeout occurred: {e}\n")
    
    # Example 3: Manual timing
    manual_timeout_example()
    
    # Example 4: TaskTimer for monitoring
    print("\n--- Example 4: Monitoring with TaskTimer ---")
    with TaskTimer("monitoring_task", timeout_seconds=5) as timer:
        for i in range(3):
            print(f"  Iteration {i+1}... ({timer.elapsed_seconds:.2f}s elapsed)")
            time.sleep(1)
    
    print(f"✓ Task completed in {timer.elapsed_seconds:.2f}s")
