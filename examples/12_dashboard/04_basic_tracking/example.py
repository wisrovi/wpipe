"""
Example 04: Basic Pipeline Tracking

Simple example showing how to track a basic pipeline execution.
The pipeline generates data, processes it, and outputs results.
All execution data is stored in SQLite for the dashboard.
"""

from wpipe import Pipeline


def main():
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    print("=" * 60)
    print("Example 04: Basic Pipeline Tracking")
    print("=" * 60)

    pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="data_generation",
        verbose=True,
    )

    pipeline.set_steps(
        [
            (generate_numbers, "generate_numbers", "v1.0"),
            (double_values, "double_values", "v1.0"),
            (calculate_sum, "calculate_sum", "v1.0"),
        ]
    )

    print("\n[Running Pipeline...]\n")
    result = pipeline.run({"count": 5})

    print(f"\n[Result] {result}")
    print(
        f"\n[Dashboard] Run: cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )


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
