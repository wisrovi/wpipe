"""
Example 05: For loop with data accumulation

Demonstrates how For can accumulate data across iterations.
"""

from wpipe import For, Pipeline


def collect_data(data):
    iteration = data.get("_loop_iteration", 0)
    data["items"] = data.get("items", [])
    data["items"].append(f"item_{iteration}")
    data["total"] = data.get("total", 0) + iteration * 10
    return data


def main():
    pipe = Pipeline(pipeline_name="data_accumulation_example", verbose=False)
    pipe.set_steps(
        [
            (lambda d: {"items": [], "total": 0}, "init", "v1"),
            For(
                iterations=4,
                steps=[
                    (collect_data, "collect", "v1"),
                ],
            ),
        ]
    )

    result = pipe.run({})
    print(f"Items: {result.get('items')}")
    print(f"Total: {result.get('total')}")
    print(f"Iterations: {result.get('_loop_iteration')}")

    # Items should have 4 entries (iterations 0, 1, 2, 3)
    # Total should be 0 + 10 + 20 + 30 = 60
    assert len(result["items"]) == 4, f"Expected 4 items, got {len(result['items'])}"
    assert result["total"] == 60, f"Expected 60, got {result['total']}"
    print("\nTest passed!")


if __name__ == "__main__":
    main()
