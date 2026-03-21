"""
06 Retry - Exponential Backoff

Shows retry with exponential backoff.
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
    """Runs the exponential backoff retry example pipeline."""
    pipeline = Pipeline(
        max_retries=3,
        retry_delay=0.2,
        verbose=True,
    )

    pipeline.set_steps([(failing_step, "Failing", "v1.0")])

    try:
        _ = pipeline.run({})
    except Exception as e:
        print(f"Failed after retries: {type(e).__name__}")


if __name__ == "__main__":
    main()
