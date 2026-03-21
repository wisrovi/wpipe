"""
03 Condition - Multiple Steps in Branch

Shows running multiple steps in each branch.
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_value(data):
    return {"value": 10}


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
    pipeline.set_steps(
        [
            (get_value, "Get Value", "v1.0"),
            condition,
        ]
    )

    print("Test 1: value = 10 (> 0)")
    result1 = pipeline.run({})
    print(f"Result keys: {list(result1.keys())}")


if __name__ == "__main__":
    main()
