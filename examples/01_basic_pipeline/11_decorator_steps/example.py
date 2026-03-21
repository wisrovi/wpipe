"""
Basic Pipeline - Decorator Steps

Using decorator pattern with pipeline steps.
"""

from wpipe import Pipeline


def logger(func):
    """Decorator to log function calls.

    Args:
        func: Function to wrap.

    Returns:
        Wrapped function with logging.
    """

    def wrapper(data: dict) -> dict:
        """Log function call and result.

        Args:
            data: Input data dictionary.

        Returns:
            Result from wrapped function.
        """
        print(f"  [LOG] Calling {func.__name__}")
        result = func(data)
        print(f"  [LOG] {func.__name__} returned: {result}")
        return result

    return wrapper


@logger
def step_a(data: dict) -> dict:
    """Add 1 to the value.

    Args:
        data: Dictionary containing 'value' key.

    Returns:
        Dictionary with 'a' key.

    Example:
        >>> step_a({"value": 5})
        {"a": 6}
    """
    return {"a": data.get("value", 0) + 1}


@logger
def step_b(data: dict) -> dict:
    """Multiply a by 2.

    Args:
        data: Dictionary containing 'a' key.

    Returns:
        Dictionary with 'b' key.

    Example:
        >>> step_b({"a": 6})
        {"b": 12}
    """
    return {"b": data.get("a", 0) * 2}


def main() -> None:
    """Run the decorator steps example.

    Demonstrates:
        - Using decorators with pipeline steps
        - Logging step execution
        - Preserving step functionality
    """
    pipeline = Pipeline(verbose=False)
    pipeline.set_steps(
        [
            (step_a, "Step A", "v1.0"),
            (step_b, "Step B", "v1.0"),
        ]
    )
    result = pipeline.run({"value": 5})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
