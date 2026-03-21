"""
01 Error Handling - Basic Exception

The simplest error handling example - catching a ValueError.
"""

from wpipe import Pipeline
from wpipe.exception import TaskError


def valid_step(data):
    return {"value": 10}


def failing_step(data):
    raise ValueError("Something went wrong!")


def next_step(data):
    return {"processed": True}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (valid_step, "Valid Step", "v1.0"),
            (failing_step, "Failing Step", "v1.0"),
            (next_step, "Next Step", "v1.0"),
        ]
    )

    result = pipeline.run({})

    if "error" in result:
        print(f"Error captured in result: {result['error']}")
    else:
        print(f"Pipeline completed: {result}")


if __name__ == "__main__":
    main()
