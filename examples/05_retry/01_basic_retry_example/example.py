"""
01 Retry - Basic Retry on Failure

The simplest retry example - retry when a function fails.
"""

from wpipe import Pipeline
import time


def unreliable_step(data):
    raise ConnectionError("Network error!")


def recovery_step(data):
    return {"status": "recovered"}


def main():
    pipeline = Pipeline(max_retries=3, retry_delay=0.1, verbose=True)

    pipeline.set_steps(
        [
            (unreliable_step, "Unreliable Step", "v1.0"),
        ]
    )

    try:
        result = pipeline.run({})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed after retries: {e}")


if __name__ == "__main__":
    main()
