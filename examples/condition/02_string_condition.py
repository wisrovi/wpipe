"""
02 Condition - String Based Condition

Shows using string conditions like 'status == "active"'.
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_status(data):
    return {"status": "active", "user": "john"}


def activate_user(data):
    return {"message": "User activated"}


def deactivate_user(data):
    return {"message": "User deactivated"}


def main():
    condition = Condition(
        expression='status == "active"',
        branch_true=[(activate_user, "Activate", "v1.0")],
        branch_false=[(deactivate_user, "Deactivate", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_status, "Get Status", "v1.0"),
            condition,
        ]
    )

    print("Test 1: status = active")
    result1 = pipeline.run({})
    print(f"Result: {result1}")


if __name__ == "__main__":
    main()
