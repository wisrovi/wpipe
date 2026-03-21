"""
02 Condition - String Based Condition

Shows using string conditions like 'status == "active"'.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def activate_user(data):
    return {"status": "active", "message": "User activated"}


def deactivate_user(data):
    return {"status": "inactive", "message": "User deactivated"}


def main():
    condition = Condition(
        expression='status == "active"',
        branch_true=[(activate_user, "Activate", "v1.0")],
        branch_false=[(deactivate_user, "Deactivate", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_condition(condition)

    print("Test 1: status = active")
    result1 = pipeline.run({"status": "active"})
    print(f"Result: {result1}")

    print("\nTest 2: status = pending")
    result2 = pipeline.run({"status": "pending"})
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
