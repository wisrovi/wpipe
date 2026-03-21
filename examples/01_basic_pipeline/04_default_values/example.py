"""
Basic Pipeline - Default Values

Using get() with default values for safe data access.
"""

from wpipe import Pipeline


def step_with_defaults(data: dict) -> dict:
    """Process data with default values for missing keys.

    Args:
        data: Dictionary that may contain 'value' and 'multiplier' keys.

    Returns:
        Dictionary with 'result' key containing value * multiplier.

    Example:
        >>> step_with_defaults({})
        {"result": 200}
        >>> step_with_defaults({"value": 10, "multiplier": 3})
        {"result": 30}
    """
    value = data.get("value", 100)
    multiplier = data.get("multiplier", 2)
    return {"result": value * multiplier}


def process_result(data: dict) -> dict:
    """Process result with default value handling.

    Args:
        data: Dictionary containing 'result' key.

    Returns:
        Dictionary with 'status' and 'value' keys.

    Example:
        >>> process_result({"result": 200})
        {"status": "completed", "value": 2000}
    """
    result = data.get("result", 0)
    return {"status": "completed", "value": result * 10}


def main() -> None:
    """Run the default values example.

    Demonstrates:
        - Using get() with default values
        - Safe handling of missing data
        - Chaining steps with default values
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step_with_defaults, "Step with Defaults", "v1.0"),
            (process_result, "Process Result", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Result: {result}")
    assert result["result"] == 200
    assert result["value"] == 2000


if __name__ == "__main__":
    main()
