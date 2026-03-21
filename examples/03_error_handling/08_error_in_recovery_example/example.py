"""08 Error Handling - Recovery After Error

Shows recovery mechanism after step failure.
"""

from typing import Any

from wpipe import Pipeline


def failing_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that intentionally fails.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises RuntimeError.

    Example:
        >>> failing_step({})
        Traceback (most recent call last):
            ...
        RuntimeError: Step failed
    """
    raise RuntimeError("Step failed")


def recovery_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that recovers after error.

    Args:
        data: Input data dictionary with optional 'error' key.

    Returns:
        Dictionary with recovery status and error info.

    Example:
        >>> result = recovery_step({"error": "test"})
        >>> print(result)
        {'recovered': True, 'error': 'test'}
    """
    return {"recovered": True, "error": data.get("error")}


def main() -> None:
    """Run the recovery after error example.

    Demonstrates how recovery steps can access error information.

    Example:
        >>> main()  # doctest: +SKIP
        Result has error: True
    """
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([(failing_step, "Failing", "v1.0")])
    result = pipeline.run({})
    print(f"Result has error: {'error' in result}")


if __name__ == "__main__":
    main()
