"""
03 Condition - Multiple Steps in Branch

Shows running multiple steps in each branch.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def step1(data):
    return {"step1": "done"}


def step2(data):
    return {"step2": "done"}


def step3(data):
    return {"step3": "done"}


def step4(data):
    return {"step4": "done"}


def main():
    condition = Condition(
        expression="value > 0",
        branch_true=[
            (step1, "Step 1", "v1.0"),
            (step2, "Step 2", "v1.0"),
        ],
        branch_false=[
            (step3, "Step 3", "v1.0"),
            (step4, "Step 4", "v1.0"),
        ],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_condition(condition)

    print("Test 1: value = 10 (> 0)")
    result1 = pipeline.run({"value": 10})
    print(f"Result keys: {list(result1.keys())}")

    print("\nTest 2: value = -5 (< 0)")
    result2 = pipeline.run({"value": -5})
    print(f"Result keys: {list(result2.keys())}")


if __name__ == "__main__":
    main()
