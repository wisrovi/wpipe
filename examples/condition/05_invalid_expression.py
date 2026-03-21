"""
05 Condition - Invalid Expression Handling

Shows how invalid condition expressions are handled.
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_data(data):
    return {"value": 5}


def valid_step(data):
    return {"result": "success"}


def main():
    condition = Condition(
        expression="nonexistent_field > 10",
        branch_true=[(valid_step, "Valid Step", "v1.0")],
        branch_false=[],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_data, "Get Data", "v1.0"),
            condition,
        ]
    )

    print("Testing with missing field in data:")
    try:
        result = pipeline.run({})
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
