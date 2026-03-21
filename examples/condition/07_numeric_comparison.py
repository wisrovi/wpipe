"""
07 Condition - Numeric Comparisons

Shows various numeric comparison operators.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition

def get_value(data):
    return {"value": 75}

def step_gt(data):
    return {"result": "greater"}

def step_lt(data):
    return {"result": "less"}

def main():
    condition = Condition(
        expression="value >= 70",
        branch_true=[(step_gt, "Greater or Equal", "v1.0")],
        branch_false=[(step_lt, "Less", "v1.0")],
    )
    
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (get_value, "Get Value", "v1.0"),
        condition,
    ])
    
    result = pipeline.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
