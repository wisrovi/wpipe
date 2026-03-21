"""
05 Retry - No Retry by Default

Shows that without max_retries, no retry happens.
"""

from wpipe import Pipeline


def failing_step(data):
    raise ConnectionError("Network error")


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (failing_step, "Failing Step", "v1.0"),
        ]
    )

    try:
        result = pipeline.run({})
    except Exception as e:
        print(f"Failed without retry: {type(e).__name__}")


if __name__ == "__main__":
    main()
