"""
06 Condition - Complex Expression

Shows using complex boolean expressions.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_data(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch multiple numeric values for complex condition evaluation.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with x, y, z values for condition testing.

    Example:
        >>> result = get_data({})
        >>> print(result)
        {'x': 10, 'y': 20, 'z': 5}
    """
    return {"x": 10, "y": 20, "z": 5}


def step_a(data: dict[str, Any]) -> dict[str, Any]:
    """Step executed when complex condition evaluates to true.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating branch A was taken.

    Example:
        >>> result = step_a({})
        >>> print(result)
        {'branch': 'A'}
    """
    return {"branch": "A"}


def step_b(data: dict[str, Any]) -> dict[str, Any]:
    """Step executed when complex condition evaluates to false.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating branch B was taken.

    Example:
        >>> result = step_b({})
        >>> print(result)
        {'branch': 'B'}
    """
    return {"branch": "B"}


def main() -> None:
    """Run the complex expression example demonstrating boolean operators.

    Creates a pipeline with a condition that uses multiple boolean
    operators (and) to combine multiple comparisons into a single
    expression: x > 5 and y > 10 and z < 10.

    Example:
        >>> main()
        Result: {...}
    """
    condition = Condition(
        expression="x > 5 and y > 10 and z < 10",
        branch_true=[(step_a, "Step A", "v1.0")],
        branch_false=[(step_b, "Step B", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_data, "Get Data", "v1.0"),
            condition,
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
