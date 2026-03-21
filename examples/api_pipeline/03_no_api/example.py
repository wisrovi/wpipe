"""
03 API Pipeline - Pipeline Without API

Shows running pipeline without API configuration (local-only mode).
Useful for testing or when API server is not available.
"""

from wpipe import Pipeline


def process_items(data: dict) -> dict:
    """Process items from input data.

    Args:
        data: Dictionary with 'items' key.

    Returns:
        Dictionary with 'processed' count and 'items' list.
    """
    items: list[int] = data.get("items", [])
    return {"processed": len(items), "items": items}


def calculate_stats(data: dict) -> dict:
    """Calculate statistics from processed items.

    Args:
        data: Dictionary with 'items' list.

    Returns:
        Dictionary with 'count', 'total', and 'average'.
    """
    items: list[int] = data.get("items", [])
    total: int = sum(items)
    count: int = len(items)
    average: float = total / count if count > 0 else 0.0
    return {"count": count, "total": total, "average": average}


def main() -> None:
    """Run the no-API example.

    Demonstrates:
        - Pipeline runs without api_config
        - All steps execute locally
        - Data aggregation through steps
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (process_items, "Process Items", "v1.0"),
            (calculate_stats, "Calculate Stats", "v1.0"),
        ]
    )

    result = pipeline.run({"items": [10, 20, 30, 40, 50]})
    print(f"Result: {result}")
    assert result["count"] == 5
    assert result["total"] == 150


if __name__ == "__main__":
    main()
