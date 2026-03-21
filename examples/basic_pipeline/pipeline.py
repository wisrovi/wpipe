"""
Basic Pipeline Example

This example demonstrates how to create and run a simple pipeline
with multiple steps using functions and classes.
"""

from wpipe.pipe import Pipeline


def step_1(data):
    """First step: Multiply input by 2."""
    x = data.get("x", 0)
    return {"x1": x * 2}


def step_2(data):
    """Second step: Add 10 to the result."""
    x1 = data.get("x1", 0)
    return {"x2": x1 + 10}


def step_3(data):
    """Third step: Square the result."""
    x2 = data.get("x2", 0)
    return {"x3": x2**2}


class FinalStep:
    """Class-based step that combines results."""

    def __call__(self, data):
        x1 = data.get("x1", 0)
        x3 = data.get("x3", 0)
        return {"final": x1 + x3}


def main():
    """Run the basic pipeline example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step_1, "Multiply by 2", "v1.0"),
            (step_2, "Add 10", "v1.0"),
            (step_3, "Square", "v1.0"),
            (FinalStep(), "Combine Results", "v1.0"),
        ]
    )

    result = pipeline.run({"x": 5})

    assert result["x1"] == 10, "Step 1 failed"
    assert result["x2"] == 20, "Step 2 failed"
    assert result["x3"] == 400, "Step 3 failed"
    assert result["final"] == 410, "Final step failed"

    print(f"Pipeline result: {result}")
    print("All assertions passed!")


if __name__ == "__main__":
    main()
