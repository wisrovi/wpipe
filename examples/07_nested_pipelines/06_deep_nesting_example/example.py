"""
06 Nested Pipelines - Deep Nesting

Shows deeply nested pipeline structure.
"""


from wpipe import Pipeline


def step_a(data: dict) -> dict:
    """Step A in pipeline 1.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with a result.

    Example:
        >>> result = step_a({})
        >>> assert result == {"a": 1}
    """
    return {"a": 1}


def step_b(data: dict) -> dict:
    """Step B in pipeline 2.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with b result.

    Example:
        >>> result = step_b({})
        >>> assert result == {"b": 2}
    """
    return {"b": 2}


def step_c(data: dict) -> dict:
    """Step C in pipeline 3.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with c result.

    Example:
        >>> result = step_c({})
        >>> assert result == {"c": 3}
    """
    return {"c": 3}


def main() -> None:
    """Run the deep nesting example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        P3: P1...
        P3: P2...
        P3: C...
        Result: {...}
    """
    p1: Pipeline = Pipeline(verbose=False)
    p1.set_steps([(step_a, "A", "v1.0")])

    p2: Pipeline = Pipeline(verbose=False)
    p2.set_steps([(step_b, "B", "v1.0")])

    p3: Pipeline = Pipeline(verbose=True)
    p3.set_steps(
        [
            (p1.run, "P1", "v1.0"),
            (p2.run, "P2", "v1.0"),
            (step_c, "C", "v1.0"),
        ]
    )

    result: dict = p3.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
