"""
03 Condition - Multiple Steps in Branch

Shows running multiple steps in each branch.
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_value(data: dict[str, Any]) -> dict[str, Any]:
    """Fetch a numeric value for condition evaluation.

    Args:
        data: Input data dictionary (unused in this function).

    Returns:
        Dictionary with a positive value for testing.

    Example:
        >>> result = get_value({})
        >>> print(result)
        {'value': 10}
    """
    return {"value": 10}


def step1(data: dict[str, Any]) -> dict[str, Any]:
    """First step in the true branch.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating step1 completion.

    Example:
        >>> result = step1({})
        >>> print(result)
        {'step1': 'done'}
    """
    return {"step1": "done"}


def step2(data: dict[str, Any]) -> dict[str, Any]:
    """Second step in the true branch.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating step2 completion.

    Example:
        >>> result = step2({})
        >>> print(result)
        {'step2': 'done'}
    """
    return {"step2": "done"}


def step3(data: dict[str, Any]) -> dict[str, Any]:
    """First step in the false branch.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating step3 completion.

    Example:
        >>> result = step3({})
        >>> print(result)
        {'step3': 'done'}
    """
    return {"step3": "done"}


def step4(data: dict[str, Any]) -> dict[str, Any]:
    """Second step in the false branch.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating step4 completion.

    Example:
        >>> result = step4({})
        >>> print(result)
        {'step4': 'done'}
    """
    return {"step4": "done"}


def main() -> None:
    """Run the multiple steps example demonstrating chained steps in branches.

    Creates a pipeline with a condition where each branch contains multiple
    steps that execute sequentially when that branch is taken.

    Example:
        >>> main()
        Test 1: value = 10 (> 0)
        Result keys: [...]
    """
    condition = Condition(
        expression="value > 0",
        branch_true=[
            (step1, "Step 1", "v1.0"),
            (step2, "Step 2", "v1.0"),
        ],
        branch_false=[
            (step3, "Step 3", "v1.0"),
            (step4, "Step 4", "v1.0"),
        ],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_value, "Get Value", "v1.0"),
            condition,
        ]
    )

    print("Test 1: value = 10 (> 0)")
    result1 = pipeline.run({})
    print(f"Result keys: {list(result1.keys())}")


if __name__ == "__main__":
    main()
