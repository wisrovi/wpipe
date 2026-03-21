"""
Basic Pipeline - Lambda Functions

Using lambda functions as pipeline steps.
"""

from wpipe import Pipeline


def main() -> None:
    """Run the lambda steps example.

    Demonstrates:
        - Using lambda functions as pipeline steps
        - Chaining lambda transformations
        - Quick inline transformations
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (lambda d: {"x2": d.get("value", 0) * 2}, "Double", "v1.0"),
            (lambda d: {"x4": d.get("x2", 0) * 2}, "Quadruple", "v1.0"),
            (lambda d: {"final": d.get("x4", 0) + 10}, "Add 10", "v1.0"),
        ]
    )

    result = pipeline.run({"value": 5})
    print(f"Result: {result}")
    assert result["final"] == 30


if __name__ == "__main__":
    main()
