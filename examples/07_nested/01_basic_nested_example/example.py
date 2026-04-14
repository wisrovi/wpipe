"""
01 Nested Pipelines - Basic Nested Pipeline

The simplest nested pipeline example - one pipeline inside another.
"""

from wpipe import Pipeline


def inner_step1(data: dict) -> dict:
    """Step in the inner pipeline.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with inner1 result.

    Example:
        >>> result = inner_step1({})
        >>> assert result == {"inner1": "done"}
    """
    return {"inner1": "done"}


def inner_step2(data: dict) -> dict:
    """Step in the inner pipeline.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with inner2 result.

    Example:
        >>> result = inner_step2({})
        >>> assert result == {"inner2": "done"}
    """
    return {"inner2": "done"}


def outer_step(data: dict) -> dict:
    """Step in the outer pipeline.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with outer result.

    Example:
        >>> result = outer_step({})
        >>> assert result == {"outer": "done"}
    """
    return {"outer": "done"}


def main() -> None:
    """Run the basic nested pipeline example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        Outer Pipeline: Inner Pipeline...
        Outer Pipeline: Outer Step...
        Result: {...}
    """
    inner_pipeline: Pipeline = Pipeline(verbose=False)
    inner_pipeline.set_steps(
        [
            (inner_step1, "Inner Step 1", "v1.0"),
            (inner_step2, "Inner Step 2", "v1.0"),
        ]
    )

    outer_pipeline: Pipeline = Pipeline(verbose=True)
    outer_pipeline.set_steps(
        [
            (inner_pipeline.run, "Inner Pipeline", "v1.0"),
            (outer_step, "Outer Step", "v1.0"),
        ]
    )

    result: dict = outer_pipeline.run({})

    print(f"Result: {result}")
    assert "inner1" in result
    assert "inner2" in result
    assert "outer" in result


if __name__ == "__main__":
    main()
