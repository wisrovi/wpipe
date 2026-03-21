"""
08 Retry - Partial Pipeline Failure

Shows retry behavior when some steps fail.
"""

from wpipe import Pipeline

def step1(data):
    return {"step1": "done"}

def step2(data):
    raise ConnectionError("Network error")

def step3(data):
    return {"step3": "done"}

def main():
    pipeline = Pipeline(
        max_retries=2,
        retry_delay=0.1,
        verbose=True
    )
    
    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
        (step3, "Step 3", "v1.0"),
    ])
    
    try:
        result = pipeline.run({})
    except Exception as e:
        print(f"Pipeline failed: {type(e).__name__}")

if __name__ == "__main__":
    main()
