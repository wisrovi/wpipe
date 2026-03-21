"""
09 Retry - Retry Counter

Shows accessing retry count in step.
"""

from wpipe import Pipeline

retry_count = 0

def counting_step(data):
    global retry_count
    retry_count += 1
    if retry_count < 3:
        raise ConnectionError(f"Attempt {retry_count}")
    return {"success": True, "attempts": retry_count}

def main():
    pipeline = Pipeline(
        max_retries=3,
        retry_delay=0.1,
        verbose=True
    )
    
    pipeline.set_steps([(counting_step, "Counting Step", "v1.0")])
    
    result = pipeline.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
