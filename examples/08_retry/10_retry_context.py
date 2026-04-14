"""
10 Retry - Retry Context Information

Shows accessing retry context in step.
"""

from wpipe import Pipeline


def step_with_context(data):
    return {"retry_info": "success"}


def main():
    pipeline = Pipeline(max_retries=2, retry_delay=0.1, verbose=True)

    pipeline.set_steps([(step_with_context, "Context Step", "v1.0")])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
