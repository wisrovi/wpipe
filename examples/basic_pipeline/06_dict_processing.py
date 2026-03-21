"""
06 Pipeline - Dictionary Processing

Shows processing dictionaries and lists within pipeline steps.
"""

from wpipe import Pipeline


def process_items(data):
    items = data.get("items", [])
    processed = [{"name": item["name"], "value": item["price"] * 1.1} for item in items]
    return {"processed_items": processed, "count": len(processed)}


def calculate_total(data):
    items = data.get("processed_items", [])
    total = sum(item["value"] for item in items)
    return {"total": total}


def apply_discount(data):
    total = data.get("total", 0)
    discount = data.get("discount", 0)
    final = total * (1 - discount / 100)
    return {"final_price": round(final, 2)}


def main():
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
