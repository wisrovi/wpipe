"""
10 Error Handling - Error Code Handling

Shows handling specific error codes.
"""

from wpipe import Pipeline


def failing_with_code(data):
    raise ValueError("Validation error")


def main():
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([(failing_with_code, "Failing", "v1.0")])
    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
