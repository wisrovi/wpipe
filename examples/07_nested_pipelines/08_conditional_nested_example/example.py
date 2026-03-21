"""
08 Nested Pipelines - Conditional Nested

Shows nested pipeline with condition selection.
"""


from wpipe import Pipeline


def get_type(data: dict) -> dict:
    """Determines the type for processing.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with type result.

    Example:
        >>> result = get_type({})
        >>> assert result == {"type": "A"}
    """
    return {"type": "A"}


def process_a(data: dict) -> dict:
    """Processes type A.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with processed result.

    Example:
        >>> result = process_a({"type": "A"})
        >>> assert result == {"processed": "A"}
    """
    return {"processed": "A"}


def process_b(data: dict) -> dict:
    """Processes type B.

    Args:
        data: Input data dictionary.

    Returns:
        Dictionary with processed result.

    Example:
        >>> result = process_b({"type": "B"})
        >>> assert result == {"processed": "B"}
    """
    return {"processed": "B"}


def main() -> None:
    """Run the conditional nested example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        Type A:
        Inner A: Process A...
        Result: {...}
        <BLANKLINE>
        Type B:
        Inner B: Process B...
        Result: {...}
    """
    inner_a: Pipeline = Pipeline(verbose=False)
    inner_a.set_steps([(process_a, "Process A", "v1.0")])

    inner_b: Pipeline = Pipeline(verbose=False)
    inner_b.set_steps([(process_b, "Process B", "v1.0")])

    print("Type A:")
    result: dict = inner_a.run({"type": "A"})
    print(f"Result: {result}")

    print("\nType B:")
    result = inner_b.run({"type": "B"})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
