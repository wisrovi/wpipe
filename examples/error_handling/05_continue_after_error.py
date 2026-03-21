"""
05 Error Handling - Finally Block Behavior

Shows that pipeline continues even when errors occur.
"""

from wpipe import Pipeline


def step1(data):
    return {"result": 100}


def failing_step(data):
    raise ValueError("Intentional failure")


def final_step(data):
    return {"final": "executed"}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
            (failing_step, "Failing Step", "v1.0"),
            (final_step, "Final Step", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Result contains step1: {'result' in result}")
    print(f"Error captured: {'error' in result}")
    print(f"Final step executed: {'final' in result}")


if __name__ == "__main__":
    main()
