"""
Basic Pipeline - Multiple Runs

Running same pipeline with different inputs.
"""

from wpipe import Pipeline


def transform(data: dict) -> dict:
    """Transform value by doubling.

    Args:
        data: Dictionary containing 'value' key.

    Returns:
        Dictionary with 'transformed' key.

    Example:
        >>> transform({"value": 5})
        {"transformed": 10}
    """
    return {"transformed": data["value"] * 2}


def validate(data: dict) -> dict:
    """Validate transformed value is positive.

    Args:
        data: Dictionary containing 'transformed' key.

    Returns:
        Dictionary with 'valid' key.

    Example:
        >>> validate({"transformed": 10})
        {"valid": True}
    """
    return {"valid": data["transformed"] > 0}


def format_output(data: dict) -> dict:
    """Format output as string.

    Args:
        data: Dictionary containing 'transformed' and 'valid' keys.

    Returns:
        Dictionary with 'output' key.

    Example:
        >>> format_output({"transformed": 10, "valid": True})
        {"output": "Value is 10, valid: True"}
    """
    return {"output": f"Value is {data['transformed']}, valid: {data['valid']}"}


def run_for_value(value: int) -> dict:
    """Run pipeline for a specific value.

    Args:
        value: Input value to process.

    Returns:
        Dictionary containing pipeline result.
    """
    pipeline = Pipeline(verbose=False)
    pipeline.set_steps(
        [
            (transform, "Transform", "v1.0"),
            (validate, "Validate", "v1.0"),
            (format_output, "Format", "v1.0"),
        ]
    )
    return pipeline.run({"value": value})


def main() -> None:
    """Run the multiple runs example.

    Demonstrates:
        - Reusing pipeline with different inputs
        - Processing multiple values
        - Collecting results from multiple runs
    """
    values = [5, 10, 15, 20]
    results = [run_for_value(v) for v in values]

    for i, r in enumerate(results):
        print(f"Input: {values[i]} -> {r['output']}")
        assert r["valid"] is True


if __name__ == "__main__":
    main()
