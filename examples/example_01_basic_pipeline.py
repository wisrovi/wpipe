"""
Example: Basic Pipeline Execution

This example demonstrates how to create and execute a basic pipeline
without API connectivity. It's perfect for local workflows.
"""

from wpipe.pipe import Pipeline


def step_1(data: dict) -> dict:
    """First step: Process initial input."""
    x = data.get("x", 0)
    return {"x1": x + 10}


def step_2(data: dict) -> dict:
    """Second step: Multiply result."""
    x1 = data.get("x1", 0)
    return {"x2": x1 * 2}


def step_3(data: dict) -> dict:
    """Third step: Combine results."""
    x1 = data.get("x1", 0)
    x2 = data.get("x2", 0)
    return {"x3": x1 + x2}


class FinalStep:
    """Final step as a class with __call__ method."""

    def __call__(self, data: dict) -> dict:
        x2 = data.get("x2", 0)
        x3 = data.get("x3", 0)
        return {"final_result": x2 + x3}


def main():
    """Execute the basic pipeline."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step_1, "Step 1 - Add", "v1.0"),
            (step_2, "Step 2 - Multiply", "v1.0"),
            (step_3, "Step 3 - Combine", "v1.0"),
            (FinalStep(), "Step 4 - Final", "v1.0"),
        ]
    )

    result = pipeline.run({"x": 5})
    print(f"Pipeline result: {result}")

    assert "x1" in result
    assert "x2" in result
    assert "x3" in result
    assert "final_result" in result

    assert result["x1"] == 15
    assert result["x2"] == 30
    assert result["x3"] == 45
    assert result["final_result"] == 75

    print("All assertions passed!")


if __name__ == "__main__":
    main()
