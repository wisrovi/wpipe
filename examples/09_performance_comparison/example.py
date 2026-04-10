"""
Example 09: Performance Comparison

Demonstrates comparing two pipeline executions.
Shows how to identify performance regressions between runs.
"""

import time
from wpipe import Pipeline, PipelineTracker


def main():
    db_path = "comparison_example.db"
    config_dir = "./configs"

    print("=" * 60)
    print("Example 09: Performance Comparison")
    print("=" * 60)

    tracker = PipelineTracker(db_path, config_dir)

    # Run Pipeline A (baseline - faster)
    print("\n[Run A: Baseline - Fast Algorithm]")
    p1 = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="algorithm_v1",
        verbose=False,
    )
    p1.set_steps(
        [
            (load_data_fast, "load", "v1.0"),
            (process_fast, "process", "v1.0"),
            (output_result, "output", "v1.0"),
        ]
    )
    result_a = p1.run({"count": 100})
    print(f"  Pipeline ID: {p1.pipeline_id}")
    print(f"  Result: {result_a}")

    # Run Pipeline B (slower - new algorithm with overhead)
    print("\n[Run B: New Algorithm - With Overhead]")
    p2 = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="algorithm_v2",
        verbose=False,
    )
    p2.set_steps(
        [
            (load_data_slow, "load", "v1.0"),
            (process_slow, "process", "v1.0"),
            (output_result, "output", "v1.0"),
        ]
    )
    result_b = p2.run({"count": 100})
    print(f"  Pipeline ID: {p2.pipeline_id}")
    print(f"  Result: {result_b}")

    # Compare stats
    print("\n[Comparing Executions]")

    stats = tracker.get_stats()
    if stats:
        print(f"\n  Total Executions: {stats.get('total_executions', 0)}")
        print(f"  Successful: {stats.get('completed', 0)}")
        print(f"  Failed: {stats.get('errors', 0)}")

    print("\n  Top Slow Steps:")
    slow_steps = tracker.get_top_slow_steps(limit=5)
    for step in slow_steps:
        print(f"    - {step['step_name']}: {step.get('avg_duration_ms', 0):.1f}ms avg")

    print(
        f"\n[Dashboard] Run: python -m wpipe.dashboard --db {db_path} --config-dir {config_dir} --open"
    )


# Fast algorithm functions
def load_data_fast(d):
    """Load data quickly."""
    import time

    time.sleep(0.1)
    return {"data": list(range(d.get("count", 100)))}


def process_fast(d):
    """Process data quickly."""
    import time

    time.sleep(0.2)
    return {"processed": [x * 2 for x in d["data"]]}


# Slow algorithm functions
def load_data_slow(d):
    """Load data with overhead."""
    import time

    time.sleep(0.2)  # Slower
    return {"data": list(range(d.get("count", 100)))}


def process_slow(d):
    """Process data with overhead."""
    import time

    time.sleep(0.4)  # Slower
    validated = []
    for x in d["data"]:
        time.sleep(0.001)  # Small delay per item
        validated.append(x * 2)
    return {"processed": validated}


def output_result(d):
    """Output result."""
    return {"output": d.get("processed", d.get("result", []))}


if __name__ == "__main__":
    main()
