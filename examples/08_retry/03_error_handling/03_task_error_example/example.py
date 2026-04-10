"""03 Error Handling - Using TaskError Directly

Shows using TaskError exception directly for custom error handling.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.exception import Codes, TaskError


def validate_input(data: dict[str, Any]) -> dict[str, Any]:
    """Validate that input value is positive.

    Args:
        data: Input data dictionary with optional 'value' key.

    Returns:
        Dictionary with validated value.

    Raises:
        TaskError: If value is negative.

    Example:
        >>> result = validate_input({"value": 10})
        >>> print(result)
        {'validated': 10}
        >>> validate_input({"value": -5})
        Traceback (most recent call last):
            ...
        wpipe.exception.TaskError: Value must be positive
    """
    value = data.get("value", 0)
    if value < 0:
        raise TaskError("Value must be positive", Codes.VALIDATION_ERROR)
    return {"validated": value}


def process(data: dict[str, Any]) -> dict[str, Any]:
    """Process validated input data.

    Args:
        data: Input data dictionary with 'validated' key.

    Returns:
        Dictionary with processed result.

    Example:
        >>> result = process({"validated": 5})
        >>> print(result)
        {'result': 10}
    """
    return {"result": data["validated"] * 2}


def main() -> None:
    """Run the TaskError example.

    Demonstrates using TaskError with validation and error codes.

    Example:
        >>> main()  # doctest: +SKIP
        Testing with positive value:
        Result: {'validated': 10, 'result': 20}
        Testing with negative value:
        Result: {'error': TaskError('Value must be positive', code=1001)}
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (validate_input, "Validate Input", "v1.0"),
            (process, "Process", "v1.0"),
        ]
    )

    print("Testing with positive value:")
    result = pipeline.run({"value": 10})
    print(f"Result: {result}")

    print("\nTesting with negative value:")
    pipeline2 = Pipeline(verbose=True)
    pipeline2.set_steps(
        [
            (validate_input, "Validate Input", "v1.0"),
            (process, "Process", "v1.0"),
        ]
    )
    result2 = pipeline2.run({"value": -5})
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
