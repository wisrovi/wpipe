"""
19 Concurrent Workers

Demonstrates multiple workers running concurrently with API tracking.
Each worker should have unique ID and operate independently.

What it evaluates:
- Multiple concurrent pipelines
- Unique worker identification
- Independent execution
- Thread-safe operations
"""

import concurrent.futures
import time

from wpipe import Pipeline


def process_task(data: dict) -> dict:
    """Process task for a worker.

    Args:
        data: Input data dictionary containing worker_id, task_id, and value.

    Returns:
        Dictionary with worker and task info plus result.

    Example:
        >>> process_task({"worker_id": "w1", "task_id": "t1", "value": 10})
        {'worker_id': 'w1', 'task_id': 't1', 'result': 20}
    """
    time.sleep(0.01)
    return {
        "worker_id": data.get("worker_id"),
        "task_id": data.get("task_id"),
        "result": data.get("value", 0) * 2,
    }


def worker_pipeline(worker_name: str, task_id: str, value: int) -> dict:
    """Create and run a pipeline for a single worker.

    Args:
        worker_name: Unique name identifier for the worker.
        task_id: Unique identifier for the task.
        value: Numeric value to process.

    Returns:
        Dictionary with worker pipeline execution result.

    Example:
        >>> worker_pipeline("worker_1", "task_a", 10)
        {'worker_id': 'worker_1', 'task_id': 'task_a', 'result': 20}
    """
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "concurrent_token",
    }

    pipeline = Pipeline(worker_name=worker_name, api_config=api_config, verbose=False)

    pipeline.set_steps([(process_task, "Process", "v1.0")])
    return pipeline.run({"worker_id": worker_name, "task_id": task_id, "value": value})


def main() -> None:
    """Run the concurrent workers example pipeline."""
    workers: list[tuple[str, str, int]] = [
        ("worker_1", "task_a", 10),
        ("worker_2", "task_b", 20),
        ("worker_3", "task_c", 30),
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures: list[concurrent.futures.Future[dict]] = [
            executor.submit(worker_pipeline, name, task, val)
            for name, task, val in workers
        ]
        results: list[dict] = [
            f.result() for f in concurrent.futures.as_completed(futures)
        ]

    for r in results:
        print(f"Worker {r['worker_id']}: {r['result']}")

    assert len(results) == 3


if __name__ == "__main__":
    main()
