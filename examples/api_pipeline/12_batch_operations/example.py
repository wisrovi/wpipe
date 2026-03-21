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


def validate_batch(data):
    """Validate batch of items."""
    items = data.get("items", [])
    valid = [item for item in items if item > 0]
    return {"valid_items": valid, "total": len(items), "valid_count": len(valid)}


def transform_batch(data):
    """Transform valid items in batch."""
    valid = data.get("valid_items", [])
    transformed = [item * 2 for item in valid]
    return {"transformed_items": transformed, "original_count": len(valid)}


def aggregate_results(data):
    """Aggregate transformed results."""
    items = data.get("transformed_items", [])
    return {"final_items": items, "sum": sum(items), "count": len(items)}


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "batch_token"}

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
