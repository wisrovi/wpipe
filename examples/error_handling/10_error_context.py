"""
10 Error Handling - Error Context

Shows accessing error context information.
"""

from wpipe import Pipeline

def failing_step(data):
    raise RuntimeError("Contextual error")

def main():
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([(failing_step, "Failing", "v1.0")])
    result = pipeline.run({})
    print(f"Error in result: {'error' in result}")
    if "error" in result:
        print(f"Error message: {result['error']}")

if __name__ == "__main__":
    main()
