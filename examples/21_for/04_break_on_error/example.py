"""
Example 04: For loop that captures errors

Demonstrates how For captures errors during execution without stopping.
The error is stored in the data for inspection.
"""

from wpipe import For, Pipeline


def may_fail(data):
    counter = data.get("counter", 0) + 1
    if counter >= 3:
        raise ValueError(f"Failed at iteration {counter}")
    data["counter"] = counter
    return data


def main():
    pipe = Pipeline(pipeline_name="break_on_error_example", verbose=False)
    pipe.set_steps(
        [
            (lambda d: {"counter": 0}, "init", "v1"),
            For(
                iterations=5,
                steps=[
                    (may_fail, "may_fail", "v1"),
                ],
            ),
        ]
    )

    result = pipe.run({})
    print(f"Counter: {result.get('counter')}")
    print(f"Error: {result.get('error')}")
    print(f"Iterations: {result.get('_loop_iteration')}")

    # Error should be captured, counter should be 2 (fails at 3rd iteration)
    assert "error" in result
    assert result.get("counter") == 2
    print("\nTest passed!")


if __name__ == "__main__":
    main()
