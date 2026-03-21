"""
09 Error Handling - Partial Results

Shows accessing partial results after error.
"""

from wpipe import Pipeline

def step1(data):
    return {"step1": "done"}

def failing_step(data):
    raise ValueError("Step 2 failed")

def step3(data):
    return {"step3": "done"}

def main():
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (failing_step, "Step 2", "v1.0"),
        (step3, "Step 3", "v1.0"),
    ])
    result = pipeline.run({})
    print(f"Step 1 completed: {'step1' in result}")
    print(f"Error present: {'error' in result}")

if __name__ == "__main__":
    main()
