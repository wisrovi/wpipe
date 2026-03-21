"""
Basic Pipeline - Data Aggregation

Accumulating data across pipeline steps.
"""

from wpipe import Pipeline


def initialize(data: dict) -> dict:
    """Initialize aggregation data structure.

    Args:
        data: Input dictionary (not used).

    Returns:
        Dictionary with empty results list and count 0.

    Example:
        >>> initialize({})
        {"results": [], "count": 0}
    """
    return {"results": [], "count": 0}


def add_item_1(data: dict) -> dict:
    """Add first item to results.

    Args:
        data: Dictionary containing 'results' and 'count' keys.

    Returns:
        Dictionary with updated results and incremented count.

    Example:
        >>> add_item_1({"results": [], "count": 0})
        {"results": [{"item": 1, "value": 100}], "count": 1}
    """
    results = data.get("results", [])
    results.append({"item": 1, "value": 100})
    return {"results": results, "count": data.get("count", 0) + 1}


def add_item_2(data: dict) -> dict:
    """Add second item to results.

    Args:
        data: Dictionary containing 'results' and 'count' keys.

    Returns:
        Dictionary with updated results and incremented count.

    Example:
        >>> add_item_2({"results": [{"item": 1, "value": 100}], "count": 1})
        {"results": [{"item": 1, "value": 100}, {"item": 2, "value": 200}], "count": 2}
    """
    results = data.get("results", [])
    results.append({"item": 2, "value": 200})
    return {"results": results, "count": data.get("count", 0) + 1}


def summarize(data: dict) -> dict:
    """Summarize aggregated data.

    Args:
        data: Dictionary containing 'results' and 'count' keys.

    Returns:
        Dictionary with 'summary' key containing summary string.

    Example:
        >>> summarize({"results": [{"value": 100}, {"value": 200}], "count": 2})
        {"summary": "Processed 2 items, total: 300"}
    """
    results = data.get("results", [])
    total = sum(r["value"] for r in results)
    return {"summary": f"Processed {data['count']} items, total: {total}"}


def main() -> None:
    """Run the data aggregation example.

    Demonstrates:
        - Initializing data structures
        - Accumulating data across steps
        - Summarizing collected data
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (initialize, "Initialize", "v1.0"),
            (add_item_1, "Add Item 1", "v1.0"),
            (add_item_2, "Add Item 2", "v1.0"),
            (summarize, "Summarize", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Result: {result}")
    assert result["count"] == 2


if __name__ == "__main__":
    main()
