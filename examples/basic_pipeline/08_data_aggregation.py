"""
08 Pipeline - Data Aggregation

Shows accumulating data across pipeline steps.
"""

from wpipe import Pipeline


def initialize(data):
    return {"results": [], "count": 0}


def add_item_1(data):
    results = data.get("results", [])
    results.append({"item": 1, "value": 100})
    return {"results": results, "count": data.get("count", 0) + 1}


def add_item_2(data):
    results = data.get("results", [])
    results.append({"item": 2, "value": 200})
    return {"results": results, "count": data.get("count", 0) + 1}


def add_item_3(data):
    results = data.get("results", [])
    results.append({"item": 3, "value": 300})
    return {"results": results, "count": data.get("count", 0) + 1}


def summarize(data):
    results = data.get("results", [])
    total = sum(r["value"] for r in results)
    return {"summary": f"Processed {data['count']} items, total: {total}"}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (initialize, "Initialize", "v1.0"),
            (add_item_1, "Add Item 1", "v1.0"),
            (add_item_2, "Add Item 2", "v1.0"),
            (add_item_3, "Add Item 3", "v1.0"),
            (summarize, "Summarize", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Result: {result}")
    assert result["count"] == 3


if __name__ == "__main__":
    main()
