"""
08 Condition - Equality Checks

Shows equality and inequality checks.
"""

from wpipe import Pipeline
from wpipe.pipe import Condition

def get_status(data):
    return {"status": "active"}

def process_active(data):
    return {"processed": "active"}

def process_inactive(data):
    return {"processed": "inactive"}

def main():
    condition = Condition(
        expression='status == "active"',
        branch_true=[(process_active, "Process Active", "v1.0")],
        branch_false=[(process_inactive, "Process Inactive", "v1.0")],
    )
    
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (get_status, "Get Status", "v1.0"),
        condition,
    ])
    
    result = pipeline.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
