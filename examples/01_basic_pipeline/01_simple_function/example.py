"""
Basic Pipeline - Simple Function Pipeline

The simplest pipeline example. Shows basic pipeline creation with sequential functions.
"""

from wpipe import Pipeline


def multiply_by_two(data: dict) -> dict:
    """Multiply input value by 2.

    Args:
        data: Dictionary containing 'input' key with numeric value.

    Returns:
        Dictionary with 'value' key containing doubled input.

    Example:
        >>> multiply_by_two({"input": 5})
        {"value": 10}
    """
    return {"value": data["input"] * 2}


def add_ten(data: dict) -> dict:
    """Add 10 to the value in data.

    Args:
        data: Dictionary containing 'value' key.

    Returns:
        Dictionary with updated 'value' key.

    Example:
        >>> add_ten({"value": 10})
        {"value": 20}
    """
    return {"value": data["value"] + 10}


def square(data: dict) -> dict:
    """Square the value in data.

    Args:
        data: Dictionary containing 'value' key.

    Returns:
        Dictionary with 'result' key containing squared value.

    Example:
        >>> square({"value": 20})
        {"result": 400}
    """
    return {"result": data["value"] ** 2}


def main() -> None:
    """Run the simple function pipeline example.

    Demonstrates:
        - Creating Pipeline instance
        - Adding function steps
        - Running pipeline with input data
        - Sequential data transformation
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (multiply_by_two, "Multiply by 2", "v1.0"),
            (add_ten, "Add 10", "v1.0"),
            (square, "Square", "v1.0"),
        ]
    )

    result = pipeline.run({"input": 5})

    print(f"Input: 5 -> Output: {result}")
    assert result["result"] == 400


if __name__ == "__main__":
    main()
