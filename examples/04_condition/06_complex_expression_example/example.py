"""
06 Condition - Complex Expression

Shows using complex boolean expressions.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition

def get_data(data):
    return {"x": 10, "y": 20, "z": 5}

def step_a(data):
    return {"branch": "A"}

def step_b(data):
    return {"branch": "B"}

def main():
    condition = Condition(
        expression="x > 5 and y > 10 and z < 10",
        branch_true=[(step_a, "Step A", "v1.0")],
        branch_false=[(step_b, "Step B", "v1.0")],
    )
    
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (get_data, "Get Data", "v1.0"),
        condition,
    ])
    
    result = pipeline.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
