"""
Parallel I/O-bound tasks example.

Demonstrates executing multiple I/O-bound tasks (like API calls) in parallel
to achieve 3x+ speedup compared to sequential execution.
"""

import time

from wpipe.parallel import ExecutionMode, ParallelExecutor


def fetch_user_data(context):
    """Simulate fetching user data from API."""
    print("[Fetch User] Starting...")
    time.sleep(1)
    print("[Fetch User] ✓ Completed")
    return {"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]}


def fetch_posts(context):
    """Simulate fetching posts from API."""
    print("[Fetch Posts] Starting...")
    time.sleep(1)
    print("[Fetch Posts] ✓ Completed")
    return {"posts": [{"id": 101, "title": "Post 1"}]}


def fetch_comments(context):
    """Simulate fetching comments from API."""
    print("[Fetch Comments] Starting...")
    time.sleep(1)
    print("[Fetch Comments] ✓ Completed")
    return {"comments": [{"id": 1001, "text": "Great!"}]}


def aggregate_data(context):
    """Aggregate all fetched data."""
    print("[Aggregate] Combining data...")
    return {
        "total_items": (
            len(context.get("users", []))
            + len(context.get("posts", []))
            + len(context.get("comments", []))
        ),
        "status": "complete",
    }


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PARALLEL I/O-BOUND TASKS EXAMPLE")
    print("=" * 60)

    executor = ParallelExecutor(max_workers=3)

    executor.add_step("fetch_users", fetch_user_data, mode=ExecutionMode.IO_BOUND)
    executor.add_step("fetch_posts", fetch_posts, mode=ExecutionMode.IO_BOUND)
    executor.add_step("fetch_comments", fetch_comments, mode=ExecutionMode.IO_BOUND)
    executor.add_step(
        "aggregate",
        aggregate_data,
        depends_on=["fetch_users", "fetch_posts", "fetch_comments"],
    )

    start = time.time()
    result = executor.execute({})
    elapsed = time.time() - start

    print("\n✓ Results:")
    print(f"  Time: {elapsed:.2f}s (vs 4s sequential = {4/elapsed:.1f}x speedup)")
    print(f"  Total items: {result['total_items']}")
    print("=" * 60 + "\n")
