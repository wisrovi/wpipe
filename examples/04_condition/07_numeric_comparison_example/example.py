"""
07 Condition - Numeric Comparisons

Shows various numeric comparison operators.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_value(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch a numeric value for comparison testing.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with a value for testing comparisons.

    Example:
        >>> result = get_value({})
        >>> print(result)
        {'value': 75}
    """
    return {"value": 75}


def step_gt(data: dict[str, Any]) -> dict[str, Any]:
    """Step executed when value is greater than or equal to threshold.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating the comparison result.

    Example:
        >>> result = step_gt({})
        >>> print(result)
        {'result': 'greater'}
    """
    return {"result": "greater"}


def step_lt(data: dict[str, Any]) -> dict[str, Any]:
    """Step executed when value is less than threshold.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating the comparison result.

    Example:
        >>> result = step_lt({})
        >>> print(result)
        {'result': 'less'}
    """
    return {"result": "less"}


def main() -> None:
    """Run the numeric comparison example demonstrating >= operator.

    Creates a pipeline with a condition that uses the greater-than-or-equal
    operator (>=) to compare a numeric value against a threshold.

    Example:
        >>> main()
        Result: {...}
    """
    condition = Condition(
        expression="value >= 70",
        branch_true=[(step_gt, "Greater or Equal", "v1.0")],
        branch_false=[(step_lt, "Less", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_value, "Get Value", "v1.0"),
            condition,
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
