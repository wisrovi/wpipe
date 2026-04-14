"""04 Error Handling - Error in Middle of Pipeline

Shows error handling when failure occurs in the middle of the pipeline.
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


def step2(data: dict[str, Any]) -> dict[str, Any]:
    """Middle step that raises RuntimeError.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises RuntimeError.

    Example:
        >>> step2({})
        Traceback (most recent call last):
            ...
        RuntimeError: Step 2 failed!
    """
    raise RuntimeError("Step 2 failed!")


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


def step4(data: dict[str, Any]) -> dict[str, Any]:
    """Fourth step (never reached when step2 fails).

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating step completion.

    Example:
        >>> result = step4({})
        >>> print(result)
        {'step4': 'done'}
    """
    return {"step4": "done"}


def main() -> None:
    """Run the middle error example.

    Demonstrates how pipeline stops execution when a step fails.

    Example:
        >>> main()  # doctest: +SKIP
        Step 1 completed: True
        Step 2 error: RuntimeError: Step 2 failed!
        Step 3 completed: False
        Step 4 completed: False
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
            (step2, "Step 2", "v1.0"),
            (step3, "Step 3", "v1.0"),
            (step4, "Step 4", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Step 1 completed: {'step1' in result}")
    print(f"Step 2 error: {result.get('error', 'No error')}")
    print(f"Step 3 completed: {'step3' in result}")
    print(f"Step 4 completed: {'step4' in result}")


if __name__ == "__main__":
    main()
