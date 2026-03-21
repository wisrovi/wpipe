"""
01 Condition - Basic Conditional Branch

The simplest condition example - choose branch based on data value.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def step_a(data):
    return {"branch": "A", "value": data.get("value", 0) * 2}


def step_b(data):
    return {"branch": "B", "value": data.get("value", 0) + 10}


def final_step(data):
    return {"final": f"Processed by {data.get('branch', 'unknown')}"}


def main():
    condition = Condition(
        expression="value > 50",
        branch_true=[(step_a, "Step A", "v1.0")],
        branch_false=[(step_b, "Step B", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_condition(condition)
    pipeline.set_steps([(final_step, "Final", "v1.0")])

    print("Test 1: value = 30 (< 50, goes to B)")
    result1 = pipeline.run({"value": 30})
    print(f"Result: {result1}")

    print("\nTest 2: value = 80 (> 50, goes to A)")
    result2 = pipeline.run({"value": 80})
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
