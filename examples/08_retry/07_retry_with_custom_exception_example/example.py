"""
07 Retry - Custom Exception Handling

Shows retry with custom exception classes.
"""

from typing import Any

from wpipe import Pipeline


class CustomError(Exception):
    """Custom exception for demonstration purposes."""

    pass


def failing_step(data: dict[str, Any]) -> None:
    """Simulates a step that always fails with a custom error.

    Args:
        data: Pipeline data dictionary.

    Raises:
        CustomError: Always raised to simulate custom failure.
    """
    raise CustomError("Custom error")


def main() -> None:
    """Runs the custom exception retry example pipeline."""
    pipeline = Pipeline(
        max_retries=2,
        retry_delay=0.1,
        retry_on_exceptions=(CustomError,),
        verbose=True,
    )

    pipeline.set_steps([(failing_step, "Failing", "v1.0")])

    try:
        _ = pipeline.run({})
    except CustomError as e:
        print(f"Custom error caught: {e}")


if __name__ == "__main__":
    main()
