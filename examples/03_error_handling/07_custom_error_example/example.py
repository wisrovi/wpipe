"""07 Error Handling - Custom Error Handler

Shows implementing custom error handling logic.
"""

from typing import Any

from wpipe import Pipeline


def step_with_error(data: dict[str, Any]) -> dict[str, Any]:
    """Step that fails when fail flag is set.

    Args:
        data: Input data dictionary with optional 'fail' key.

    Returns:
        Dictionary with success flag.

    Raises:
        ValueError: If 'fail' is True in data.

    Example:
        >>> result = step_with_error({})
        >>> print(result)
        {'success': True}
        >>> step_with_error({"fail": True})
        Traceback (most recent call last):
            ...
        ValueError: Intentional failure
    """
    if data.get("fail"):
        raise ValueError("Intentional failure")
    return {"success": True}


def error_handler(data: dict[str, Any]) -> dict[str, Any]:
    """Handle errors from failed steps.

    Args:
        data: Input data dictionary with optional 'error' key.

    Returns:
        Dictionary with handled status and error info.

    Example:
        >>> result = error_handler({"error": "test"})
        >>> print(result)
        {'handled': True, 'error': 'test'}
    """
    return {"handled": True, "error": data.get("error")}


def main() -> None:
    """Run the custom error handler example.

    Demonstrates how custom error handling can be implemented.

    Example:
        >>> main()  # doctest: +SKIP
        Result: {'error': ValueError('Intentional failure')}
    """
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([(step_with_error, "Step", "v1.0")])

    result = pipeline.run({"fail": True})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
