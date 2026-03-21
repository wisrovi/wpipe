"""
04 Nested Pipelines - Reusing Pipeline Objects

Shows how to reuse the same pipeline object multiple times.
"""


from wpipe import Pipeline


def process_item(data: dict) -> dict:
    """Processes an item by doubling its value.

    Args:
        data: Input data dictionary containing item.

    Returns:
        Dictionary with processed result.

    Example:
        >>> result = process_item({"item": 5})
        >>> assert result == {"processed": 10}
    """
    item: int = data.get("item", 0)
    return {"processed": item * 2}


def main() -> None:
    """Run the pipeline reuse example.

    Example:
        >>> main()  # doctest: +ELLIPSIS
        Main Pipeline: Process 1...
        Main Pipeline: Process 2...
        Main Pipeline: Process 3...
        Result: {...}
    """
    reusable_pipeline: Pipeline = Pipeline(verbose=False)
    reusable_pipeline.set_steps(
        [
            (process_item, "Process Item", "v1.0"),
        ]
    )

    main_pipeline: Pipeline = Pipeline(verbose=True)
    main_pipeline.set_steps(
        [
            (reusable_pipeline.run, "Process 1", "v1.0"),
            (reusable_pipeline.run, "Process 2", "v1.0"),
            (reusable_pipeline.run, "Process 3", "v1.0"),
        ]
    )

    result: dict = main_pipeline.run({"item": 10})

    print(f"Result: {result}")
    assert result["processed"] == 20


if __name__ == "__main__":
    main()
