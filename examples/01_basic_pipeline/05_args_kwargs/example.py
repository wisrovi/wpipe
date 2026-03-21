"""
Basic Pipeline - Args and Kwargs

Passing additional arguments to pipeline steps.
"""

from wpipe import Pipeline


def transform_data(data: dict, multiplier: int = 1, offset: int = 0) -> dict:
    """Transform data with multiplier and offset.

    Args:
        data: Dictionary containing 'value' key.
        multiplier: Factor to multiply value by (default: 1).
        offset: Value to add to result (default: 0).

    Returns:
        Dictionary with 'transformed' key containing result.

    Example:
        >>> transform_data({"value": 10}, multiplier=2, offset=5)
        {"transformed": 25}
    """
    value = data.get("value", 0)
    return {"transformed": (value * multiplier) + offset}


def validate_data(data: dict, min_val: int = 0, max_val: int = 100) -> dict:
    """Validate transformed value is within range.

    Args:
        data: Dictionary containing 'transformed' key.
        min_val: Minimum allowed value (default: 0).
        max_val: Maximum allowed value (default: 100).

    Returns:
        Dictionary with 'valid' and 'value' keys.

    Example:
        >>> validate_data({"transformed": 25}, min_val=0, max_val=100)
        {"valid": True, "value": 25}
    """
    value = data.get("transformed", 0)
    in_range = min_val <= value <= max_val
    return {"valid": in_range, "value": value}


def main() -> None:
    """Run the args and kwargs example.

    Demonstrates:
        - Passing extra arguments to pipeline.run()
        - Using default parameters in steps
        - Validation with configurable ranges
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (transform_data, "Transform Data", "v1.0"),
            (validate_data, "Validate Data", "v1.0"),
        ]
    )

    result = pipeline.run({"value": 10}, multiplier=2, offset=5)

    print(f"Result: {result}")
    assert result["transformed"] == 25
    assert result["valid"] is True


if __name__ == "__main__":
    main()
