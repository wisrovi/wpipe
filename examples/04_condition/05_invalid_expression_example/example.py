"""
05 Condition - Invalid Expression Handling

Shows how invalid condition expressions are handled.
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_data(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch data without the field needed for condition.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with a value field but not the expected field.

    Example:
        >>> result = get_data({})
        >>> print(result)
        {'value': 5}
    """
    return {"value": 5}


def valid_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that would execute if condition passes.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating successful execution.

    Example:
        >>> result = valid_step({})
        >>> print(result)
        {'result': 'success'}
    """
    return {"result": "success"}


def main() -> None:
    """Run the invalid expression handling example.

    Demonstrates how the pipeline handles conditions when the referenced
    field does not exist in the data. A ValueError is raised when the
    expression references a field that is not present in the pipeline state.

    Example:
        >>> main()
        Testing with missing field in data:
        Error: ...
    """
    condition = Condition(
        expression="nonexistent_field > 10",
        branch_true=[(valid_step, "Valid Step", "v1.0")],
        branch_false=[],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_data, "Get Data", "v1.0"),
            condition,
        ]
    )

    print("Testing with missing field in data:")
    try:
        result = pipeline.run({})
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
