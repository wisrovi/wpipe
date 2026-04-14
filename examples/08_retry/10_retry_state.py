"""
10 Retry - Pipeline Retry State

Shows checking pipeline retry state.
"""

from wpipe import Pipeline


def step(data):
    return {"step": "done"}


def main():
    pipeline = Pipeline(max_retries=3, retry_delay=0.1, verbose=True)

    pipeline.set_steps([(step, "Step", "v1.0")])

    result = pipeline.run({})
    print(f"Result: {result}")
    print(f"Max retries: {pipeline.max_retries}")
    print(f"Retry delay: {pipeline.retry_delay}")


if __name__ == "__main__":
    main()
