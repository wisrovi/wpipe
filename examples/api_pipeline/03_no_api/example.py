"""
03 API Pipeline - Without API Config

Shows using pipeline without API configuration (local-only mode).
"""

from wpipe import Pipeline


def process_items(data):
    items = data.get("items", [])
    return {"processed": len(items), "items": items}


def calculate_stats(data):
    items = data.get("items", [])
    return {
        "count": len(items),
        "total": sum(items),
        "average": sum(items) / len(items) if items else 0,
    }


def main():
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
