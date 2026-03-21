"""
06 Retry - Exponential Backoff

Shows retry with exponential backoff.
"""

from wpipe import Pipeline

def failing_step(data):
    raise ConnectionError("Network error")

def main():
    pipeline = Pipeline(
        max_retries=3,
        retry_delay=0.2,
        verbose=True
    )
    
    pipeline.set_steps([(failing_step, "Failing", "v1.0")])
    
    try:
        result = pipeline.run({})
    except Exception as e:
        print(f"Failed after retries: {type(e).__name__}")

if __name__ == "__main__":
    main()
