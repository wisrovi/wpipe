"""Error Handling - Error Recovery

Shows recovering from errors gracefully.
"""

from typing import Any

from wpipe import Pipeline


def failing_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that intentionally raises ValueError.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises ValueError.

    Example:
        >>> failing_step({})
        Traceback (most recent call last):
            ...
        ValueError: Error occurred
    """
    raise ValueError("Error occurred")


def main() -> None:
    """Run the error recovery example.

    Demonstrates how errors are captured in the pipeline result.

    Example:
        >>> main()  # doctest: +SKIP
        Result: {'error': ValueError('Error occurred')}
        Has error: True
    """
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([(failing_step, "Failing Step", "v1.0")])

    result = pipeline.run({})
    print(f"Result: {result}")
    print(f"Has error: {'error' in result}")


if __name__ == "__main__":
    main()
