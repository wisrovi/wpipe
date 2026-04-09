"""
Example 01: For loop with fixed iterations

Demonstrates how to use For with a fixed number of iterations.
"""

from wpipe import For, Pipeline


def increment(data):
    data["counter"] = data.get("counter", 0) + 1
    data["value"] = data.get("value", 0) + 10
    return data


def main():
    pipe = Pipeline(pipeline_name="iterations_example", verbose=False)
    pipe.set_steps(
        [
            (lambda d: {"counter": 0, "value": 0}, "init", "v1"),
            For(
                iterations=5,
                steps=[
                    (increment, "increment", "v1"),
                ],
            ),
        ]
    )

    result = pipe.run({})
    print(f"Counter: {result.get('counter')} (expected: 5)")
    print(f"Value: {result.get('value')} (expected: 50)")
    print(f"Iterations: {result.get('_loop_iteration')}")

    assert result["counter"] == 5, "Counter should be 5"
    assert result["value"] == 50, "Value should be 50"
    print("\nTest passed!")


if __name__ == "__main__":
    main()
