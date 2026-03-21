"""
04 Condition - No Else Branch

Shows condition without else branch (branch_false).
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def premium_process(data):
    return {"processed": "premium", "discount": 0.1}


def main():
    condition = Condition(
        expression="tier == 'premium'",
        branch_true=[(premium_process, "Premium Process", "v1.0")],
        branch_false=[],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_condition(condition)

    print("Test 1: tier = premium")
    result1 = pipeline.run({"tier": "premium"})
    print(f"Result: {result1}")

    print("\nTest 2: tier = basic")
    result2 = pipeline.run({"tier": "basic"})
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
