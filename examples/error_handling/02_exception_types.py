"""
02 Error Handling - Different Exception Types

Shows handling different types of exceptions.
"""

from wpipe import Pipeline


def type_error_step(data):
    raise TypeError("Expected int, got str")


def key_error_step(data):
    raise KeyError("Missing required key")


def assertion_error_step(data):
    raise AssertionError("Validation failed")


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (type_error_step, "Type Error Step", "v1.0"),
        ]
    )

    result = pipeline.run({"value": "test"})
    print(f"Result with TypeError: {result.get('error', 'No error')}")

    pipeline2 = Pipeline(verbose=True)
    pipeline2.set_steps(
        [
            (key_error_step, "Key Error Step", "v1.0"),
        ]
    )

    result2 = pipeline2.run({})
    print(f"Result with KeyError: {result2.get('error', 'No error')}")


if __name__ == "__main__":
    main()
