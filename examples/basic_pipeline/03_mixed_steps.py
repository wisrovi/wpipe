"""
03 Basic Pipeline - Mixed Functions and Classes

Demonstrates combining functions and classes in the same pipeline.
"""

from wpipe import Pipeline


def extract_numbers(data):
    return {"numbers": [1, 2, 3, 4, 5]}


class SumNumbers:
    def __call__(self, data):
        return {"sum": sum(data["numbers"])}


def calculate_average(data):
    return {"average": data["sum"] / len(data["numbers"])}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (extract_numbers, "Extract Numbers", "v1.0"),
            (SumNumbers(), "Sum Numbers", "v1.0"),
            (calculate_average, "Calculate Average", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Result: {result}")
    assert result["sum"] == 15
    assert result["average"] == 3.0


if __name__ == "__main__":
    main()
