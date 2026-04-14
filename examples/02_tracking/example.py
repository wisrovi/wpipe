"""
Example 01: Basic Pipeline Tracking

Simple example showing how to track a basic pipeline execution.
The pipeline generates data, processes it, and outputs results.
All execution data is stored in SQLite for the dashboard.
"""

import tempfile
from pathlib import Path

from wpipe import Pipeline, PipelineTracker


def main():
    # Create temporary database
    db_path = "basic_tracking.db"
    config_dir = "./configs"

    print("=" * 60)
    print("Example 01: Basic Pipeline Tracking")
    print("=" * 60)

    # Create pipeline with tracking
    pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_generation",
        verbose=True,
    )

    # Define simple steps
    pipeline.set_steps(
        [
            (generate_numbers, "generate_numbers", "v1.0"),
            (double_values, "double_values", "v1.0"),
            (calculate_sum, "calculate_sum", "v1.0"),
        ]
    )

    # Run pipeline
    print("\n[Running Pipeline...]\n")
    result = pipeline.run({"count": 5})

    print(f"\n[Result] {result}")
    print(
        f"\n[Dashboard] Run: python -m wpipe.dashboard --db {db_path} --config-dir {config_dir} --open"
    )


# Step functions
def generate_numbers(d):
    """Generate a list of numbers."""
    count = d.get("count", 5)
    return {"numbers": list(range(1, count + 1))}


def double_values(d):
    """Double each number."""
    return {"doubled": [x * 2 for x in d["numbers"]]}


def calculate_sum(d):
    """Calculate sum of doubled values."""
    return {"sum": sum(d["doubled"]), "count": len(d["doubled"])}


if __name__ == "__main__":
    main()
