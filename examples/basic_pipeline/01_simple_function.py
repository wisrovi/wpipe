"""
01 Basic Pipeline - Simple Function Pipeline

This is the simplest possible pipeline example. It demonstrates:
- Creating a Pipeline instance
- Defining steps as simple functions
- Running the pipeline with input data

Steps are numbered from 01 to indicate progression from simple to complex.
"""

from wpipe import Pipeline


def multiply_by_two(data):
    return {"value": data["input"] * 2}


def add_ten(data):
    return {"value": data["value"] + 10}


def square(data):
    return {"result": data["value"] ** 2}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (multiply_by_two, "Multiply by 2", "v1.0"),
            (add_ten, "Add 10", "v1.0"),
            (square, "Square", "v1.0"),
        ]
    )

    result = pipeline.run({"input": 5})

    print(f"Input: 5 -> Output: {result}")
    assert result["result"] == 400


if __name__ == "__main__":
    main()
