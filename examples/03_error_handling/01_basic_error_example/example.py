"""01 Error Handling - Basic Exception

Shows the simplest error handling example - catching a ValueError.
"""

from typing import Any

from wpipe import Pipeline


def valid_step(data: dict[str, Any]) -> dict[str, Any]:
    """Process data successfully.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with processed value.

    Example:
        >>> result = valid_step({})
        >>> print(result)
        {'value': 10}
    """
    return {"value": 10}


def failing_step(data: dict[str, Any]) -> dict[str, Any]:
    """Intentionally raise a ValueError.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises ValueError.

    Example:
        >>> failing_step({})
        Traceback (most recent call last):
            ...
        ValueError: Something went wrong!
    """
    raise ValueError("Something went wrong!")


def next_step(data: dict[str, Any]) -> dict[str, Any]:
    """Process data after error recovery.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with success flag.

    Example:
        >>> result = next_step({})
        >>> print(result)
        {'processed': True}
    """
    return {"processed": True}


def main() -> None:
    """Run the basic error handling example.

    Creates a pipeline with three steps where the middle step fails.
    Demonstrates how errors are captured in the pipeline result.

    Example:
        >>> main()  # doctest: +SKIP
        Error captured in result: {...}
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (valid_step, "Valid Step", "v1.0"),
            (failing_step, "Failing Step", "v1.0"),
            (next_step, "Next Step", "v1.0"),
        ]
    )

    result = pipeline.run({})

    if "error" in result:
        print(f"Error captured in result: {result['error']}")
    else:
        print(f"Pipeline completed: {result}")


if __name__ == "__main__":
    main()
