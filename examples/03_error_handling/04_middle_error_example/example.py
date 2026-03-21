"""
04 Error Handling - Error in Middle of Pipeline

Shows error handling when failure occurs in the middle of the pipeline.
"""

from wpipe import Pipeline


def step1(data):
    return {"step1": "done"}


def step2(data):
    raise RuntimeError("Step 2 failed!")


def step3(data):
    return {"step3": "done"}


def step4(data):
    return {"step4": "done"}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
            (step2, "Step 2", "v1.0"),
            (step3, "Step 3", "v1.0"),
            (step4, "Step 4", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Step 1 completed: {'step1' in result}")
    print(f"Step 2 error: {result.get('error', 'No error')}")
    print(f"Step 3 completed: {'step3' in result}")
    print(f"Step 4 completed: {'step4' in result}")


if __name__ == "__main__":
    main()
