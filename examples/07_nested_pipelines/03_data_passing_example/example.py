"""
03 Nested Pipelines - Data Passing Between Nested Pipelines

Shows how data is passed between nested pipelines.
"""


from wpipe import Pipeline


def generate_data(data: dict) -> dict:
    """Generates initial data value.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with generated value.

    Example:
        >>> result = generate_data({})
        >>> assert result == {"value": 100}
    """
    return {"value": 100}


def transform_data(data: dict) -> dict:
    """Transforms the data value by doubling it.

    Args:
        data: Input data dictionary containing value.

    Returns:
        Dictionary with transformed value.

    Example:
        >>> result = transform_data({"value": 50})
        >>> assert result == {"transformed": 100}
    """
    return {"transformed": data.get("value", 0) * 2}


def combine_data(data: dict) -> dict:
    """Combines original and transformed values.

    Args:
        data: Input data dictionary containing value and transformed.

    Returns:
        Dictionary with combined result.

    Example:
        >>> result = combine_data({"value": 100, "transformed": 200})
        >>> assert result == {"combined": 300}
    """
    return {"combined": data.get("value", 0) + data.get("transformed", 0)}


def main() -> None:
    """Run the data passing example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        Main Pipeline: Generate Pipeline...
        Main Pipeline: Transform Pipeline...
        Main Pipeline: Combine...
        Result: {...}
    """
    gen_pipeline: Pipeline = Pipeline(verbose=False)
    gen_pipeline.set_steps(
        [
            (generate_data, "Generate", "v1.0"),
        ]
    )

    transform_pipeline: Pipeline = Pipeline(verbose=False)
    transform_pipeline.set_steps(
        [
            (transform_data, "Transform", "v1.0"),
        ]
    )

    main_pipeline: Pipeline = Pipeline(verbose=True)
    main_pipeline.set_steps(
        [
            (gen_pipeline.run, "Generate Pipeline", "v1.0"),
            (transform_pipeline.run, "Transform Pipeline", "v1.0"),
            (combine_data, "Combine", "v1.0"),
        ]
    )

    result: dict = main_pipeline.run({})

    print(f"Result: {result}")
    assert result["value"] == 100
    assert result["transformed"] == 200
    assert result["combined"] == 300


if __name__ == "__main__":
    main()
