"""
10 Pipeline - Lambda Functions

Shows using lambda functions as pipeline steps.
"""

from wpipe import Pipeline


def main():
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
    assert result["final"] == 50


if __name__ == "__main__":
    main()
