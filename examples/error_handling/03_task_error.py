"""
03 Error Handling - Using TaskError Directly

Shows using TaskError exception directly.
"""

from wpipe import Pipeline
from wpipe.exception import TaskError, Codes


def validate_input(data):
    value = data.get("value", 0)
    if value < 0:
        raise TaskError("Value must be positive", Codes.VALIDATION_ERROR)
    return {"validated": value}


def process(data):
    return {"result": data["validated"] * 2}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (validate_input, "Validate Input", "v1.0"),
            (process, "Process", "v1.0"),
        ]
    )

    print("Testing with positive value:")
    result = pipeline.run({"value": 10})
    print(f"Result: {result}")

    print("\nTesting with negative value:")
    pipeline2 = Pipeline(verbose=True)
    pipeline2.set_steps(
        [
            (validate_input, "Validate Input", "v1.0"),
            (process, "Process", "v1.0"),
        ]
    )
    result2 = pipeline2.run({"value": -5})
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
