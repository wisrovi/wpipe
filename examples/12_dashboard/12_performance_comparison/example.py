"""
Example 09: Performance Comparison

Demonstrates comparing two pipeline executions.
Shows how to identify performance regressions between runs.
"""

import random

from wpipe import Pipeline, PipelineTracker


def main():
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    print("=" * 60)
    print("Example 12: Performance Comparison")
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
            (load_data_slow, "load", "v2.0"),
            (process_slow, "process", "v2.0"),
            (output_result, "output", "v2.0"),
        ]
    )
    result_b = p2.run({"count": 100})
    print(f"  Pipeline ID: {p2.pipeline_id}")
    print(f"  Result: {result_b}")

    # Compare the two executions
    print("\n[Comparing Executions]")
    comparison = tracker.compare_pipelines(p1.pipeline_id, p2.pipeline_id)

    print(f"\n  Duration A: {comparison['pipeline_a']['duration_ms']:.2f}ms")
    print(f"  Duration B: {comparison['pipeline_b']['duration_ms']:.2f}ms")
    print(
        f"  Difference: {comparison['duration_diff_ms']:.2f}ms ({comparison['duration_diff_percent']:+.1f}%)"
    )

    print("\n  Step Comparison:")
    for step in comparison["steps_comparison"]:
        if step["in_a"] and step["in_b"]:
            status = "⚠️ CHANGED" if step.get("status_changed") else "✓ Same"
            print(
                f"    - {step['step_name']}: {step['duration_a']:.1f}ms -> {step['duration_b']:.1f}ms {status}"
            )
        elif step["in_a"]:
            print(f"    - {step['step_name']}: Removed in B")
        else:
            print(f"    - {step['step_name']}: Added in B")

    print(f"\n[Comparison ID] {comparison['comparison_id']}")
    print(
        f"\n[Dashboard] Run: cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
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
    # Extra validation step that takes time
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
