"""
07 Nested Pipelines - Parallel Execution

Shows multiple nested pipelines executed in sequence.
"""

from wpipe import Pipeline


def process_a(data: dict) -> dict:
    """Processes value for pipeline A.

    Args:
        data: Input data dictionary containing value.

    Returns:
        Dictionary with a result.

    Example:
        >>> result = process_a({"value": 10})
        >>> assert result == {"a": 10}
    """
    return {"a": data.get("value", 0)}


def process_b(data: dict) -> dict:
    """Processes value for pipeline B (doubles it).

    Args:
        data: Input data dictionary containing value.

    Returns:
        Dictionary with b result.

    Example:
        >>> result = process_b({"value": 10})
        >>> assert result == {"b": 20}
    """
    return {"b": data.get("value", 0) * 2}


def combine(data: dict) -> dict:
    """Combines results from both pipelines.

    Args:
        data: Input data dictionary containing a and b.

    Returns:
        Dictionary with combined result.

    Example:
        >>> result = combine({"a": 10, "b": 20})
        >>> assert result == {"combined": 30}
    """
    return {"combined": data.get("a", 0) + data.get("b", 0)}


def main() -> None:
    """Run the parallel nested example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        Main: Pipeline A...
        Main: Pipeline B...
        Main: Combine...
        Result: {...}
    """
    p1: Pipeline = Pipeline(verbose=False)
    p1.set_steps([(process_a, "Process A", "v1.0")])

    p2: Pipeline = Pipeline(verbose=False)
    p2.set_steps([(process_b, "Process B", "v1.0")])

    main_p: Pipeline = Pipeline(verbose=True)
    main_p.set_steps(
        [
            (p1.run, "Pipeline A", "v1.0"),
            (p2.run, "Pipeline B", "v1.0"),
            (combine, "Combine", "v1.0"),
        ]
    )

    result: dict = main_p.run({"value": 10})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
