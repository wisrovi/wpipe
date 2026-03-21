"""
10 Condition - None Check

Shows checking for None values.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_data(data):
    return {"name": None, "value": 10}


def handle_null(data):
    return {"result": "null_name"}


def handle_valid(data):
    return {"result": "valid_name"}


def main():
    condition = Condition(
        expression="name is None",
        branch_true=[(handle_null, "Handle Null", "v1.0")],
        branch_false=[(handle_valid, "Handle Valid", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_data, "Get Data", "v1.0"),
            condition,
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
