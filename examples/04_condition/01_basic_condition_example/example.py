"""
01 Condition - Basic Conditional Branch

The simplest condition example - choose branch based on data value.
IMPORTANT: Condition must come AFTER a step that provides the data.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition


def fetch_data(data):
    return {"value": 80, "type": "A"}


def step_a(data):
    return {"branch": "A", "result": data.get("value", 0) * 2}


def step_b(data):
    return {"branch": "B", "result": data.get("value", 0) + 10}


def final_step(data):
    return {"final": f"Processed by {data.get('branch', 'unknown')}"}


def main():
    condition = Condition(
        expression="value > 50",
        branch_true=[(step_a, "Step A", "v1.0")],
        branch_false=[(step_b, "Step B", "v1.0")],
    )

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (fetch_data, "Fetch Data", "v1.0"),
            condition,
            (final_step, "Final", "v1.0"),
        ]
    )

    print("Test 1: value = 80 (> 50, goes to A)")
    result1 = pipeline.run({})
    print(f"Result: {result1}")

    print("\nTest 2: value = 30 (< 50, goes to B)")
    pipeline2 = Pipeline(verbose=True)
    pipeline2.set_steps(
        [
            (fetch_data, "Fetch Data", "v1.0"),
            condition,
            (final_step, "Final", "v1.0"),
        ]
    )
    result2 = pipeline2.run({})
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
