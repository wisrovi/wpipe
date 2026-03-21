"""
Error Handling - Error Recovery

Shows recovering from errors gracefully.
"""

from wpipe import Pipeline


def failing_step(data):
    raise ValueError("Error occurred")


def main():
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([(failing_step, "Failing Step", "v1.0")])
    
    result = pipeline.run({})
    print(f"Result: {result}")
    print(f"Has error: {'error' in result}")


if __name__ == "__main__":
    main()
