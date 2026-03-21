"""
Basic Pipeline - Async Steps

Pipeline steps with async-like processing (simulated).
"""

from wpipe import Pipeline


def step_a(data: dict) -> dict:
    """Process step A.

    Args:
        data: Dictionary containing 'value' key.

    Returns:
        Dictionary with 'step' and 'value' keys.

    Example:
        >>> step_a({"value": 5})
        {"step": "A", "value": 5}
    """
    return {"step": "A", "value": data.get("value", 0)}


def step_b(data: dict) -> dict:
    """Process step B (double value).

    Args:
        data: Dictionary containing 'value' key.

    Returns:
        Dictionary with 'step' and 'value' keys.

    Example:
        >>> step_b({"value": 5})
        {"step": "B", "value": 10}
    """
    return {"step": "B", "value": data.get("value", 0) * 2}


def step_c(data: dict) -> dict:
    """Process step C (add 10).

    Args:
        data: Dictionary containing 'value' key.

    Returns:
        Dictionary with 'step' and 'value' keys.

    Example:
        >>> step_c({"value": 5})
        {"step": "C", "value": 15}
    """
    return {"step": "C", "value": data.get("value", 0) + 10}


def main() -> None:
    """Run the async pipeline example.

    Demonstrates:
        - Sequential step execution
        - Multiple transformations
        - Async-like processing pattern
    """
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (step_a, "Step A", "v1.0"),
            (step_b, "Step B", "v1.0"),
            (step_c, "Step C", "v1.0"),
        ]
    )

    result = pipeline.run({"value": 5})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
