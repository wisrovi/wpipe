"""
05 Nested Pipelines - Passing Custom Data

Shows passing custom data to nested pipelines.
"""


from wpipe import Pipeline


def inner_step(data: dict) -> dict:
    """Inner pipeline step that doubles the input value.

    Args:
        data: Input data dictionary containing value.

    Returns:
        Dictionary with inner_result.

    Example:
        >>> result = inner_step({"value": 5})
        >>> assert result == {"inner_result": 10}
    """
    return {"inner_result": data.get("value", 0) * 2}


def outer_step(data: dict) -> dict:
    """Outer pipeline step that adds to inner result.

    Args:
        data: Input data dictionary containing inner_result.

    Returns:
        Dictionary with outer_result.

    Example:
        >>> result = outer_step({"inner_result": 10})
        >>> assert result == {"outer_result": 20}
    """
    return {"outer_result": data.get("inner_result", 0) + 10}


def main() -> None:
    """Run the custom data passing example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        Outer: Inner Pipeline...
        Outer: Outer...
        Result: {...}
    """
    inner: Pipeline = Pipeline(verbose=False)
    inner.set_steps([(inner_step, "Inner", "v1.0")])

    outer: Pipeline = Pipeline(verbose=True)
    outer.set_steps(
        [
            (inner.run, "Inner Pipeline", "v1.0"),
            (outer_step, "Outer", "v1.0"),
        ]
    )

    result: dict = outer.run({"value": 5})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
