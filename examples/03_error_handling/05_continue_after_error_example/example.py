"""05 Error Handling - Finally Block Behavior

Shows that pipeline continues even when errors occur.
"""

from typing import Any

from wpipe import Pipeline


def step1(data: dict[str, Any]) -> dict[str, Any]:
    """First step that completes successfully.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with result value.

    Example:
        >>> result = step1({})
        >>> print(result)
        {'result': 100}
    """
    return {"result": 100}


def failing_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that intentionally fails.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises ValueError.

    Example:
        >>> failing_step({})
        Traceback (most recent call last):
            ...
        ValueError: Intentional failure
    """
    raise ValueError("Intentional failure")


def final_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that always executes in finally block.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary indicating final execution.

    Example:
        >>> result = final_step({})
        >>> print(result)
        {'final': 'executed'}
    """
    return {"final": "executed"}


def main() -> None:
    """Run the finally block example.

    Demonstrates how pipeline ensures cleanup steps run even after errors.

    Example:
        >>> main()  # doctest: +SKIP
        Result contains step1: True
        Error captured: True
        Final step executed: True
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
            (failing_step, "Failing Step", "v1.0"),
            (final_step, "Final Step", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Result contains step1: {'result' in result}")
    print(f"Error captured: {'error' in result}")
    print(f"Final step executed: {'final' in result}")


if __name__ == "__main__":
    main()
