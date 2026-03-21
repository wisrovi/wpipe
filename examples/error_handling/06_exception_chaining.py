"""
06 Error Handling - Exception Chaining

Shows exception chaining with cause.
"""

from wpipe import Pipeline
from wpipe.exception import TaskError, Codes

def failing_step(data):
    raise TaskError("Original error", Codes.TASK_FAILED)

def main():
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([(failing_step, "Failing", "v1.0")])
    try:
        result = pipeline.run({})
    except Exception as e:
        print(f"Caught: {type(e).__name__}: {e}")

if __name__ == "__main__":
    main()
