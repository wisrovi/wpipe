"""02 Error Handling - Different Exception Types

Shows handling different types of exceptions in pipeline steps.
"""

from typing import Any

from wpipe import Pipeline


def type_error_step(data: dict[str, Any]) -> dict[str, Any]:
    """Raise a TypeError to simulate type mismatch.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises TypeError.

    Example:
        >>> type_error_step({"value": "test"})
        Traceback (most recent call last):
            ...
        TypeError: Expected int, got str
    """
    raise TypeError("Expected int, got str")


def key_error_step(data: dict[str, Any]) -> dict[str, Any]:
    """Raise a KeyError to simulate missing key.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises KeyError.

    Example:
        >>> key_error_step({})
        Traceback (most recent call last):
            ...
        KeyError: 'Missing required key'
    """
    raise KeyError("Missing required key")


def assertion_error_step(data: dict[str, Any]) -> dict[str, Any]:
    """Raise an AssertionError to simulate validation failure.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises AssertionError.

    Example:
        >>> assertion_error_step({})
        Traceback (most recent call last):
            ...
        AssertionError: Validation failed
    """
    raise AssertionError("Validation failed")


def main() -> None:
    """Run the different exception types example.

    Demonstrates how different exception types are handled
    uniformly by the pipeline.

    Example:
        >>> main()  # doctest: +SKIP
        Result with TypeError: TypeError: Expected int, got str
        Result with KeyError: KeyError: 'Missing required key'
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (type_error_step, "Type Error Step", "v1.0"),
        ]
    )

    result = pipeline.run({"value": "test"})
    print(f"Result with TypeError: {result.get('error', 'No error')}")

    pipeline2 = Pipeline(verbose=True)
    pipeline2.set_steps(
        [
            (key_error_step, "Key Error Step", "v1.0"),
        ]
    )

    result2 = pipeline2.run({})
    print(f"Result with KeyError: {result2.get('error', 'No error')}")


if __name__ == "__main__":
    main()
