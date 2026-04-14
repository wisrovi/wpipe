"""06 Error Handling - Exception Chaining

Shows exception chaining with cause.
"""

from typing import Any

from wpipe import Pipeline
from wpipe.exception import Codes, TaskError


def failing_step(data: dict[str, Any]) -> dict[str, Any]:
    """Raise TaskError that gets chained.

    Args:
        data: Input data dictionary.

    Returns:
        Never returns, always raises TaskError.

    Example:
        >>> failing_step({})
        Traceback (most recent call last):
            ...
        wpipe.exception.TaskError: Original error
    """
    raise TaskError("Original error", Codes.TASK_FAILED)


def main() -> None:
    """Run the exception chaining example.

    Demonstrates how TaskError is caught and chained in the pipeline.

    Example:
        >>> main()  # doctest: +SKIP
        Caught: TaskError: Original error
    """
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([(failing_step, "Failing", "v1.0")])
    try:
        pipeline.run({})
    except Exception as e:
        print(f"Caught: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
