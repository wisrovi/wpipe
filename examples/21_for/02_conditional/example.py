"""
Example 02: For loop with conditional expression

Demonstrates how to use For with a validation_expression that
controls when the loop continues. Also shows @state decorated functions.
"""

from wpipe import For, Pipeline
from wpipe.util import state


@state(name="decrement", version="v1.0")
def decrement_until_zero(data):
    data["counter"] = data.get("counter", 10) - 1
    return data


def main():
    pipe = Pipeline(pipeline_name="conditional_example", verbose=False)
    pipe.set_steps(
        [
            (lambda d: {"counter": 5}, "init", "v1"),
            For(
                validation_expression="counter > 0",
                steps=[
                    decrement_until_zero,
                ],
            ),
        ]
    )

    result = pipe.run({})
    print(f"Counter: {result.get('counter')} (expected: 0)")
    print(f"Iterations: {result.get('_loop_iteration')} (expected: 5)")

    assert result["counter"] == 0, "Counter should be 0"
    assert result["_loop_iteration"] == 5, "Should run 5 iterations"
    print("\nTest passed!")


if __name__ == "__main__":
    main()
