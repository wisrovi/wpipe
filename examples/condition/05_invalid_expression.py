"""
05 Condition - Invalid Expression Handling

Shows how invalid condition expressions are handled.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def valid_step(data):
    return {"result": "success"}


def main():
    condition = Condition(
        expression="nonexistent_field > 10",
        branch_true=[(valid_step, "Valid Step", "v1.0")],
        branch_false=[],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_condition(condition)

    print("Testing with missing field in data:")
    try:
        result = pipeline.run({"value": 5})
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
