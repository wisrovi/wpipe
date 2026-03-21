"""
Error Handling Example

This example demonstrates how to handle errors in pipelines.
The pipeline captures exceptions and stores them in the result data.
"""

from wpipe.pipe import Pipeline
from wpipe.exception import TaskError


def step_1(data):
    """First step: always succeeds."""
    return {"step1": "completed"}


def failing_step(data):
    """This step will fail with a ValueError."""
    raise ValueError("This is a simulated error")


def step_3(data):
    """This step won't run if previous step failed."""
    return {"step3": "completed"}


def main():
    """Run the error handling example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step_1, "Step 1", "v1.0"),
            (failing_step, "Failing Step", "v1.0"),
            (step_3, "Step 3", "v1.0"),
        ]
    )

    try:
        result = pipeline.run({"data": "test"})
        if "error" in result:
            print(f"Error captured: {result['error']}")
        else:
            print(f"Pipeline result: {result}")
    except TaskError as e:
        print(f"TaskError caught: {e}")


if __name__ == "__main__":
    main()
