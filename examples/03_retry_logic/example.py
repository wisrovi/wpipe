"""
Example 03: Retry Logic

Demonstrates automatic retry functionality.
The pipeline will retry failed steps up to the configured number of times.
"""

from wpipe import Pipeline


def main():
    db_path = "retry_logic.db"
    config_dir = "./configs"

    print("=" * 60)
    print("Example 03: Retry Logic")
    print("=" * 60)

    # Pipeline with retry
    pipeline = Pipeline(
        tracking_db=db_path,
        config_dir=config_dir,
        pipeline_name="retry_example",
        verbose=True,
        max_retries=3,  # Retry up to 3 times
        retry_delay=0.5,  # Wait 0.5 seconds between retries
        retry_on_exceptions=(RuntimeError,),  # Only retry on RuntimeError
    )

    pipeline.set_steps(
        [
            (prepare, "prepare", "v1.0"),
            (
                flaky_operation,
                "flaky_operation",
                "v1.0",
            ),  # Will fail twice, then succeed
            (cleanup, "cleanup", "v1.0"),
        ]
    )

    print("\n[Running Pipeline...]\n")
    print("Note: flaky_operation will fail twice before succeeding")
    print()

    result = pipeline.run({"input": "data"})

    print(f"\n[Result] {result}")
    print(
        f"\n[Dashboard] Run: python -m wpipe.dashboard --db {db_path} --config-dir {config_dir} --open"
    )


# Attempt counter for flaky function
attempt_counter = {"flaky": 0}


# Step functions
def prepare(d):
    """Prepare step."""
    print("  [prepare] Initializing...")
    return {"prepared": True}


def flaky_operation(d):
    """A flaky operation that fails twice before succeeding."""
    attempt_counter["flaky"] += 1
    attempt = attempt_counter["flaky"]

    print(f"  [flaky_operation] Attempt {attempt}...")

    if attempt < 3:
        print(f"  [flaky_operation] Failed! (attempt {attempt}/3)")
        raise RuntimeError(f"Simulated failure on attempt {attempt}")

    print(f"  [flaky_operation] Success on attempt {attempt}!")
    return {"flaky_result": "success"}


def cleanup(d):
    """Cleanup step."""
    print("  [cleanup] Finalizing...")
    return {"cleaned": True}


if __name__ == "__main__":
    main()
