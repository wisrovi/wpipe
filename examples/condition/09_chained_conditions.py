"""
09 Condition - Chained Conditions

Shows chaining multiple conditions.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition

def get_data(data):
    return {"tier": "premium", "amount": 1000}

def premium_high(data):
    return {"category": "premium_high"}

def premium_low(data):
    return {"category": "premium_low"}

def standard(data):
    return {"category": "standard"}

def main():
    condition1 = Condition(
        expression="tier == 'premium'",
        branch_true=[
            Condition(
                expression="amount > 500",
                branch_true=[(premium_high, "Premium High", "v1.0")],
                branch_false=[(premium_low, "Premium Low", "v1.0")],
            )
        ],
        branch_false=[(standard, "Standard", "v1.0")],
    )
    
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (get_data, "Get Data", "v1.0"),
        condition1,
    ])
    
    result = pipeline.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
