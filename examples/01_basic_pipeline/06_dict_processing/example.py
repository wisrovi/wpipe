"""
Basic Pipeline - Dictionary Processing

Processing complex nested data structures.
"""

from wpipe import Pipeline


def process_items(data: dict) -> dict:
    """Process items with 10% price increase.

    Args:
        data: Dictionary containing 'items' key with list of items.

    Returns:
        Dictionary with 'processed_items' and 'count' keys.

    Example:
        >>> process_items({"items": [{"name": "A", "price": 100}]})
        {"processed_items": [{"name": "A", "value": 110}], "count": 1}
    """
    items = data.get("items", [])
    processed = [{"name": item["name"], "value": item["price"] * 1.1} for item in items]
    return {"processed_items": processed, "count": len(processed)}


def calculate_total(data: dict) -> dict:
    """Calculate total value of processed items.

    Args:
        data: Dictionary containing 'processed_items' key.

    Returns:
        Dictionary with 'total' key containing sum of values.

    Example:
        >>> calculate_total({"processed_items": [{"value": 100}, {"value": 200}]})
        {"total": 300}
    """
    items = data.get("processed_items", [])
    total = sum(item["value"] for item in items)
    return {"total": total}


def apply_discount(data: dict) -> dict:
    """Apply discount to total price.

    Args:
        data: Dictionary containing 'total' and 'discount' keys.

    Returns:
        Dictionary with 'final_price' key containing discounted total.

    Example:
        >>> apply_discount({"total": 300, "discount": 10})
        {"final_price": 270.0}
    """
    total = data.get("total", 0)
    discount = data.get("discount", 0)
    final = total * (1 - discount / 100)
    return {"final_price": round(final, 2)}


def main() -> None:
    """Run the dictionary processing example.

    Demonstrates:
        - Processing list of dictionaries
        - Calculating totals
        - Applying percentage discounts
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (process_items, "Process Items", "v1.0"),
            (calculate_total, "Calculate Total", "v1.0"),
            (apply_discount, "Apply Discount", "v1.0"),
        ]
    )

    result = pipeline.run(
        {
            "items": [
                {"name": "Item1", "price": 100},
                {"name": "Item2", "price": 200},
                {"name": "Item3", "price": 50},
            ],
            "discount": 10,
        }
    )

    print(f"Result: {result}")
    assert result["count"] == 3
    assert abs(result["total"] - 385) < 0.1


if __name__ == "__main__":
    main()
