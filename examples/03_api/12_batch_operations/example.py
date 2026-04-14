"""
12 Batch Operations

Demonstrates processing data in batches through the pipeline.
Useful for handling large datasets efficiently.

What it evaluates:
- Processing multiple items in a single pipeline run
- Batch data aggregation
- Efficient data handling for bulk operations
"""

from wpipe import Pipeline


def validate_batch(data: dict) -> dict:
    """Validate batch of items.

    Args:
        data: Input data dictionary containing 'items' list.

    Returns:
        Dictionary with valid items and validation statistics.

    Example:
        >>> validate_batch({"items": [1, 2, -1, 3]})
        {'valid_items': [1, 2, 3], 'total': 4, 'valid_count': 3}
    """
    items: list = data.get("items", [])
    valid: list = [item for item in items if item > 0]
    return {"valid_items": valid, "total": len(items), "valid_count": len(valid)}


def transform_batch(data: dict) -> dict:
    """Transform valid items in batch.

    Args:
        data: Input data dictionary containing 'valid_items' list.

    Returns:
        Dictionary with transformed items and original count.

    Example:
        >>> transform_batch({"valid_items": [1, 2, 3]})
        {'transformed_items': [2, 4, 6], 'original_count': 3}
    """
    valid: list = data.get("valid_items", [])
    transformed: list = [item * 2 for item in valid]
    return {"transformed_items": transformed, "original_count": len(valid)}


def aggregate_results(data: dict) -> dict:
    """Aggregate transformed results.

    Args:
        data: Input data dictionary containing 'transformed_items' list.

    Returns:
        Dictionary with final items, sum, and count.

    Example:
        >>> aggregate_results({"transformed_items": [2, 4, 6]})
        {'final_items': [2, 4, 6], 'sum': 12, 'count': 3}
    """
    items: list = data.get("transformed_items", [])
    return {"final_items": items, "sum": sum(items), "count": len(items)}


def main() -> None:
    """Run the batch operations example pipeline."""
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "batch_token",
    }

    pipeline = Pipeline(worker_name="batch_worker", api_config=api_config, verbose=True)

    pipeline.set_steps(
        [
            (validate_batch, "Validate Batch", "v1.0"),
            (transform_batch, "Transform Batch", "v1.0"),
            (aggregate_results, "Aggregate Results", "v1.0"),
        ]
    )

    result = pipeline.run({"items": [1, 2, 3, 4, 5, -1, 6, 7, -2, 8]})

    print(f"Result: {result}")
    assert result["count"] == 8
    assert result["sum"] == 72


if __name__ == "__main__":
    main()
