"""
04 Retry - Multiple Steps with Retry

Shows retry behavior with multiple steps in pipeline.
"""

from wpipe import Pipeline


def step1(data):
    return {"step1": "done"}


def step2(data):
    raise ConnectionError("Step 2 failed")


def step3(data):
    return {"step3": "done"}


def main():
    pipeline = Pipeline(max_retries=2, retry_delay=0.1, verbose=True)

    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
            (step2, "Step 2", "v1.0"),
            (step3, "Step 3", "v1.0"),
        ]
    )

    try:
        result = pipeline.run({})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()
