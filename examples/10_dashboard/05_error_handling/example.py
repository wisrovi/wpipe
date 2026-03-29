"""
Example 02: Error Handling

Demonstrates how errors are tracked and displayed in the dashboard.
Shows different error types and how they appear in the tracking system.
"""

from wpipe import Pipeline


def main():
    db_path = "../wpipe_dashboard.db"
    config_dir = "../configs"

    print("=" * 60)
    print("Example 05: Error Handling")
    print("=" * 60)

    # Pipeline that will fail
    pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="error_example",
        verbose=True,
    )

    pipeline.set_steps(
        [
            (validate_input, "validate_input", "v1.0"),
            (process_data, "process_data", "v1.0"),  # This will fail
            (finalize, "finalize", "v1.0"),  # This won't run
        ]
    )

    print("\n[Running Pipeline...]\n")

    try:
        result = pipeline.run({"data": None})  # This will cause validation error
        print(f"\n[Result] {result}")
    except Exception as e:
        print(f"\n[Expected Error] {type(e).__name__}: {e}")
        print("\n[Info] Error is tracked in the database and visible in dashboard")

    print(
        f"\n[Dashboard] Run: cd .. && python -m wpipe.dashboard --db wpipe_dashboard.db --config-dir configs --open"
    )


# Step functions
def validate_input(d):
    """Validate input data."""
    if d.get("data") is None:
        raise ValueError("Input data cannot be None")
    return {"validated": True}


def process_data(d):
    """Process the data (won't be reached)."""
    return {"processed": True}


def finalize(d):
    """Finalize processing (won't be reached)."""
    return {"finalized": True}


if __name__ == "__main__":
    main()
