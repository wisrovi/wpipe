"""
01 Condition - Basic Conditional Branch

The simplest condition example - choose branch based on data value.
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def fetch_data(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch initial data for the pipeline.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with value and type for condition evaluation.

    Example:
        >>> result = fetch_data({})
        >>> print(result)
        {'value': 80, 'type': 'A'}
    """
    return {"value": 80, "type": "A"}


def step_a(data: dict[str, Any]) -> dict[str, Any]:
    """Process data when condition is true (value > 50).

    Args:
        data: Input data dictionary containing 'value' key.

    Returns:
        Dictionary with branch identifier and doubled value.

    Example:
        >>> result = step_a({"value": 80})
        >>> print(result)
        {'branch': 'A', 'result': 160}
    """
    return {"branch": "A", "result": data.get("value", 0) * 2}


def step_b(data: dict[str, Any]) -> dict[str, Any]:
    """Process data when condition is false (value <= 50).

    Args:
        data: Input data dictionary containing 'value' key.

    Returns:
        Dictionary with branch identifier and value increased by 10.

    Example:
        >>> result = step_b({"value": 30})
        >>> print(result)
        {'branch': 'B', 'result': 40}
    """
    return {"branch": "B", "result": data.get("value", 0) + 10}


def final_step(data: dict[str, Any]) -> dict[str, Any]:
    """Final processing step that reports which branch was used.

    Args:
        data: Input data dictionary containing 'branch' key.

    Returns:
        Dictionary with final processing message.

    Example:
        >>> result = final_step({"branch": "A"})
        >>> print(result)
        {'final': 'Processed by A'}
    """
    return {"final": f"Processed by {data.get('branch', 'unknown')}"}


def main() -> None:
    """Run the basic condition example demonstrating conditional branching.

    Creates a pipeline with a condition that evaluates 'value > 50' and
    routes execution to different branches based on the result.

    Example:
        >>> main()
        Test 1: value = 80 (> 50, goes to A)
        Result: {...}
    """
    condition = Condition(
        expression="value > 50",
        branch_true=[(step_a, "Step A", "v1.0")],
        branch_false=[(step_b, "Step B", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (fetch_data, "Fetch Data", "v1.0"),
            condition,
            (final_step, "Final", "v1.0"),
        ]
    )

    print("Test 1: value = 80 (> 50, goes to A)")
    result1 = pipeline.run({})
    print(f"Result: {result1}")

    print("\nTest 2: value = 30 (< 50, goes to B)")
    pipeline2 = Pipeline(verbose=True)
    pipeline2.set_steps(
        [
            (fetch_data, "Fetch Data", "v1.0"),
            condition,
            (final_step, "Final", "v1.0"),
        ]
    )
    result2 = pipeline2.run({})
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
