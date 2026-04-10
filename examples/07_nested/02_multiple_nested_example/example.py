"""
02 Nested Pipelines - Multiple Nested Pipelines

Shows running multiple nested pipelines in sequence.
"""

from wpipe import Pipeline


def pipeline_a_step1(data: dict) -> dict:
    """First step of pipeline A.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with a1 result.

    Example:
        >>> result = pipeline_a_step1({})
        >>> assert result == {"a1": 1}
    """
    return {"a1": 1}


def pipeline_a_step2(data: dict) -> dict:
    """Second step of pipeline A.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with a2 result.

    Example:
        >>> result = pipeline_a_step2({})
        >>> assert result == {"a2": 2}
    """
    return {"a2": 2}


def pipeline_b_step1(data: dict) -> dict:
    """First step of pipeline B.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with b1 result.

    Example:
        >>> result = pipeline_b_step1({})
        >>> assert result == {"b1": 10}
    """
    return {"b1": 10}


def pipeline_b_step2(data: dict) -> dict:
    """Second step of pipeline B.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with b2 result.

    Example:
        >>> result = pipeline_b_step2({})
        >>> assert result == {"b2": 20}
    """
    return {"b2": 20}


def final_step(data: dict) -> dict:
    """Combines results from both pipelines.

    Args:
        data: Input data dictionary containing a1 and b1 values.

    Returns:
        Dictionary with final sum result.

    Example:
        >>> result = final_step({"a1": 5, "b1": 10})
        >>> assert result == {"final": 15}
    """
    return {"final": data.get("a1", 0) + data.get("b1", 0)}


def main() -> None:
    """Run the multiple nested pipelines example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        Main Pipeline: Pipeline A...
        Main Pipeline: Pipeline B...
        Main Pipeline: Final Step...
        Result: {...}
    """
    pipeline_a: Pipeline = Pipeline(verbose=False)
    pipeline_a.set_steps(
        [
            (pipeline_a_step1, "A Step 1", "v1.0"),
            (pipeline_a_step2, "A Step 2", "v1.0"),
        ]
    )

    pipeline_b: Pipeline = Pipeline(verbose=False)
    pipeline_b.set_steps(
        [
            (pipeline_b_step1, "B Step 1", "v1.0"),
            (pipeline_b_step2, "B Step 2", "v1.0"),
        ]
    )

    main_pipeline: Pipeline = Pipeline(verbose=True)
    main_pipeline.set_steps(
        [
            (pipeline_a.run, "Pipeline A", "v1.0"),
            (pipeline_b.run, "Pipeline B", "v1.0"),
            (final_step, "Final Step", "v1.0"),
        ]
    )

    result: dict = main_pipeline.run({})

    print(f"Result: {result}")
    assert result["a1"] == 1
    assert result["a2"] == 2
    assert result["b1"] == 10
    assert result["b2"] == 20
    assert result["final"] == 11


if __name__ == "__main__":
    main()
