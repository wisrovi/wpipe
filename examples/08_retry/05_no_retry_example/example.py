"""
05 Retry - No Retry by Default

Shows that without max_retries, no retry happens.
"""

from typing import Any

from wpipe import Pipeline


def failing_step(data: dict[str, Any]) -> None:
    """Simulates a step that always fails with a network error.

    Args:
        data: Pipeline data dictionary.

    Raises:
        ConnectionError: Always raised to simulate network failure.
    """
    raise ConnectionError("Network error")


def main() -> None:
    """Runs the no-retry example demonstrating default behavior."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (failing_step, "Failing Step", "v1.0"),
        ]
    )

    try:
        _ = pipeline.run({})
    except Exception as e:
        print(f"Failed without retry: {type(e).__name__}")


if __name__ == "__main__":
    main()
