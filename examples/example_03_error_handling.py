"""
Example: Error Handling in Pipelines

This example demonstrates how to handle errors in pipeline execution
and how errors are propagated through the pipeline.
"""

from wpipe.pipe import Pipeline
from wpipe.exception import TaskError


def step_success(data: dict) -> dict:
    """A step that always succeeds."""
    return {"step1": "completed"}


def step_with_error(data: dict) -> dict:
    """A step that raises an error."""
    raise ValueError("This step encountered an error!")


def step_after_error(data: dict) -> dict:
    """This step should not be reached."""
    return {"step3": "should_not_reach"}


def validation_step(data: dict) -> dict:
    """Validation step that checks required fields."""
    if "x" not in data:
        raise ValueError("Missing required field 'x'")
    if data["x"] < 0:
        raise ValueError("Field 'x' must be non-negative")
    return {"validated": True}


def main():
    """Demonstrate error handling in pipelines."""
    print("=" * 60)
    print("Example 1: Pipeline with error in middle step")
    print("=" * 60)

    pipeline = Pipeline(verbose=True)
    pipeline.set_steps(
        [
            (step_success, "Success Step", "v1.0"),
            (step_with_error, "Error Step", "v1.0"),
            (step_after_error, "Never Runs", "v1.0"),
        ]
    )

    try:
        result = pipeline.run({})
        print(f"Result: {result}")
    except TaskError as e:
        print(f"Pipeline caught error: {e}")

    print("\n" + "=" * 60)
    print("Example 2: Pipeline with validation error")
    print("=" * 60)

    pipeline2 = Pipeline(verbose=True)
    pipeline2.set_steps(
        [
            (validation_step, "Validation", "v1.0"),
            (step_success, "Success", "v1.0"),
        ]
    )

    try:
        result = pipeline2.run({"x": -5})
        print(f"Result: {result}")
    except TaskError as e:
        print(f"Pipeline caught validation error: {e}")

    print("\n" + "=" * 60)
    print("Example 3: Successful pipeline after error handling")
    print("=" * 60)

    pipeline3 = Pipeline(verbose=True)
    pipeline3.set_steps(
        [
            (validation_step, "Validation", "v1.0"),
            (step_success, "Success", "v1.0"),
        ]
    )

    try:
        result = pipeline3.run({"x": 10})
        print(f"Result: {result}")
        print("Pipeline completed successfully!")
    except TaskError as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()
