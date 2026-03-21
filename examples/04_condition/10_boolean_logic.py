"""
10 Condition - Boolean Logic

Shows using OR and NOT operators.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_data(data):
    return {"enabled": False, "is_admin": True}


def process_authorized(data):
    return {"result": "authorized"}


def process_unauthorized(data):
    return {"result": "unauthorized"}


def main():
    condition = Condition(
        expression="enabled or is_admin",
        branch_true=[(process_authorized, "Authorized", "v1.0")],
        branch_false=[(process_unauthorized, "Unauthorized", "v1.0")],
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
