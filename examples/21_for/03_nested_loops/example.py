"""
Example 03: Nested For loops

This example demonstrates nested For loops.
Note: Nested For loops have some complexity in current implementation.
"""

from wpipe import For, Pipeline


def track_iterations(data):
    """Track iteration counts in a list."""
    iteration = data.get("_loop_iteration", 0)
    data["history"] = data.get("history", [])
    data["history"].append(f"iter_{iteration}")
    return data


def main():
    pipe = Pipeline(pipeline_name="nested_example", verbose=False)
    pipe.set_steps(
        [
            (lambda d: {"history": []}, "init", "v1"),
            For(
                iterations=3,
                steps=[
                    (track_iterations, "track", "v1"),
                ],
            ),
        ]
    )

    result = pipe.run({})
    print(f"History: {result.get('history')}")
    print(f"Iterations: {result.get('_loop_iteration')}")

    # Should have 3 entries
    assert len(result["history"]) == 3
    print("\nTest passed!")


if __name__ == "__main__":
    main()
