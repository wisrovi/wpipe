"""
Basic Pipeline - Empty Data Handling

Handling missing or empty input data.
"""

from wpipe import Pipeline


def step_a(data: dict) -> dict:
    """Process data with default value for missing key.

    Args:
        data: Dictionary that may contain 'value' key.

    Returns:
        Dictionary with 'processed' key containing doubled value.

    Example:
        >>> step_a({})
        {"processed": 0}
        >>> step_a({"value": 10})
        {"processed": 20}
    """
    value = data.get("value", 0)
    return {"processed": value * 2}


def step_b(data: dict) -> dict:
    """Process with multiplier from data or default.

    Args:
        data: Dictionary containing 'processed' and 'multiplier' keys.

    Returns:
        Dictionary with 'result' key.

    Example:
        >>> step_b({"processed": 20})
        {"result": 20}
        >>> step_b({"processed": 20, "multiplier": 3})
        {"result": 60}
    """
    value = data.get("processed", 0)
    multiplier = data.get("multiplier", 1)
    return {"result": value * multiplier}


def main() -> None:
    """Run the empty data handling example.

    Demonstrates:
        - Handling empty input data
        - Using default values
        - Graceful degradation
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step_a, "Step A", "v1.0"),
            (step_b, "Step B", "v1.0"),
        ]
    )

    result = pipeline.run({})
    print(f"Result with empty data: {result}")
    assert result["result"] == 0

    result2 = pipeline.run({"value": 10, "multiplier": 3})
    print(f"Result with data: {result2}")
    assert result2["result"] == 60


if __name__ == "__main__":
    main()
