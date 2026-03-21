"""
03 Retry - Filter Specific Exceptions

Shows retrying only specific exception types.
"""

from wpipe import Pipeline


def network_error_step(data):
    raise ConnectionError("Network timeout")


def validation_error_step(data):
    raise ValueError("Invalid input")


def main():
    pipeline = Pipeline(
        max_retries=2,
        retry_delay=0.1,
        retry_on_exceptions=(ConnectionError,),
        verbose=True,
    )

    pipeline.set_steps(
        [
            (network_error_step, "Network Step", "v1.0"),
        ]
    )

    try:
        result = pipeline.run({})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Network error - retries exhausted: {e}")

    print("\n--- Testing with ValueError (not in retry list) ---")
    pipeline2 = Pipeline(
        max_retries=2,
        retry_delay=0.1,
        retry_on_exceptions=(ConnectionError,),
        verbose=True,
    )

    pipeline2.set_steps(
        [
            (validation_error_step, "Validation Step", "v1.0"),
        ]
    )

    try:
        result = pipeline2.run({})
    except ValueError as e:
        print(f"ValueError immediately (no retry): {e}")


if __name__ == "__main__":
    main()
