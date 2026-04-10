"""
Basic parallel execution example.

Demonstrates parallel step execution with ThreadPoolExecutor.
"""

import time

from wpipe.parallel import ExecutionMode, ParallelExecutor


def fetch_data_1(context):
    """Fetch data from source 1."""
    print("  [FETCH 1] Fetching data from source 1...")
    time.sleep(1)  # Simulate I/O
    return {"data_1": [1, 2, 3, 4, 5]}


def fetch_data_2(context):
    """Fetch data from source 2."""
    print("  [FETCH 2] Fetching data from source 2...")
    time.sleep(1)  # Simulate I/O
    return {"data_2": [6, 7, 8, 9, 10]}


def fetch_data_3(context):
    """Fetch data from source 3."""
    print("  [FETCH 3] Fetching data from source 3...")
    time.sleep(1)  # Simulate I/O
    return {"data_3": [11, 12, 13, 14, 15]}


def merge_data(context):
    """Merge all fetched data (depends on all fetch steps)."""
    print("  [MERGE] Merging all data...")
    all_data = context["data_1"] + context["data_2"] + context["data_3"]
    return {"merged_data": all_data, "count": len(all_data)}


def analyze_data(context):
    """Analyze merged data."""
    print("  [ANALYZE] Analyzing data...")
    data = context["merged_data"]
    stats = {
        "sum": sum(data),
        "avg": sum(data) / len(data),
        "min": min(data),
        "max": max(data),
    }
    return {"statistics": stats}


if __name__ == "__main__":
    print("=== Parallel Execution Example ===\n")

    # Create executor
    executor = ParallelExecutor(max_workers=4)

    # Add parallel steps (can run simultaneously)
    executor.add_step("fetch_1", fetch_data_1, mode=ExecutionMode.IO_BOUND)
    executor.add_step("fetch_2", fetch_data_2, mode=ExecutionMode.IO_BOUND)
    executor.add_step("fetch_3", fetch_data_3, mode=ExecutionMode.IO_BOUND)

    # Add dependent steps
    executor.add_step(
        "merge",
        merge_data,
        depends_on=["fetch_1", "fetch_2", "fetch_3"],
    )
    executor.add_step(
        "analyze",
        analyze_data,
        depends_on=["merge"],
    )

    # Execute
    print("→ Starting parallel execution...\n")
    start = time.time()

    result = executor.execute({})

    elapsed = time.time() - start

    print(f"\n✓ Execution completed in {elapsed:.2f}s")
    print(f"  (Sequential would take ~5s)")
    print(f"  Speedup: {5.0/elapsed:.1f}x")
    print(f"\nFinal result:")
    print(f"  Statistics: {result.get('statistics')}")
    print(f"  Total count: {result.get('count')}")
