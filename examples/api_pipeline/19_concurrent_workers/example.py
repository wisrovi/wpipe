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

from wpipe import Pipeline
import concurrent.futures


def process_task(data):
    """Process task for a worker."""
    import time

    time.sleep(0.01)
    return {
        "worker_id": data.get("worker_id"),
        "task_id": data.get("task_id"),
        "result": data.get("value", 0) * 2,
    }


def worker_pipeline(worker_name, task_id, value):
    """Create and run a pipeline for a single worker."""
    api_config = {"base_url": "http://localhost:8418", "token": "concurrent_token"}

    pipeline = Pipeline(worker_name=worker_name, api_config=api_config, verbose=False)

    pipeline.set_steps([(process_task, "Process", "v1.0")])
    return pipeline.run({"worker_id": worker_name, "task_id": task_id, "value": value})


def main():
    workers = [
        ("worker_1", "task_a", 10),
        ("worker_2", "task_b", 20),
        ("worker_3", "task_c", 30),
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(worker_pipeline, name, task, val)
            for name, task, val in workers
        ]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    for r in results:
        print(f"Worker {r['worker_id']}: {r['result']}")

    assert len(results) == 3


if __name__ == "__main__":
    main()
