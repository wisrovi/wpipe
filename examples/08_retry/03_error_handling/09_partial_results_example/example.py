"""09 Error Handling - Partial Results

Shows accessing partial results after error.
"""

from typing import Any

from wpipe import Pipeline


def step1(data: dict[str, Any]) -> dict[str, Any]:
    """First step that completes successfully.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating step completion.

    Example:
        >>> result = step1({})
        >>> print(result)
        {'step1': 'done'}
    """
    return {"step1": "done"}


def failing_step(data: dict[str, Any]) -> dict[str, Any]:
    """Middle step that raises ValueError.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises ValueError.

    Example:
        >>> failing_step({})
        Traceback (most recent call last):
            ...
        ValueError: Step 2 failed
    """
    raise ValueError("Step 2 failed")


def step3(data: dict[str, Any]) -> dict[str, Any]:
    """Third step (never reached when step2 fails).

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating step completion.

    Example:
        >>> result = step3({})
        >>> print(result)
        {'step3': 'done'}
    """
    return {"step3": "done"}


def main() -> None:
    """Run the partial results example.

    Demonstrates how to access partial results after pipeline error.

    Example:
        >>> main()  # doctest: +SKIP
        Step 1 completed: True
        Error present: True
    """
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
            (failing_step, "Step 2", "v1.0"),
            (step3, "Step 3", "v1.0"),
        ]
    )
    result = pipeline.run({})
    print(f"Step 1 completed: {'step1' in result}")
    print(f"Error present: {'error' in result}")


if __name__ == "__main__":
    main()
