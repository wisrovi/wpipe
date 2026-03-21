"""
04 Condition - No Else Branch

Shows condition without else branch (branch_false).
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def get_tier(data):
    return {"tier": "premium", "name": "test"}


def premium_process(data):
    return {"processed": "premium", "discount": 0.1}


def main():
    condition = Condition(
        expression="tier == 'premium'",
        branch_true=[(premium_process, "Premium Process", "v1.0")],
        branch_false=[],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (get_tier, "Get Tier", "v1.0"),
            condition,
        ]
    )

    print("Test 1: tier = premium")
    result1 = pipeline.run({})
    print(f"Result: {result1}")


if __name__ == "__main__":
    main()
