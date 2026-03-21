"""
07 Retry - Custom Exception Handling

Shows retry with custom exception classes.
"""

from wpipe import Pipeline

class CustomError(Exception):
    pass

def failing_step(data):
    raise CustomError("Custom error")

def main():
    pipeline = Pipeline(
        max_retries=2,
        retry_delay=0.1,
        retry_on_exceptions=(CustomError,),
        verbose=True
    )
    
    pipeline.set_steps([(failing_step, "Failing", "v1.0")])
    
    try:
        result = pipeline.run({})
    except CustomError as e:
        print(f"Custom error caught: {e}")

if __name__ == "__main__":
    main()
