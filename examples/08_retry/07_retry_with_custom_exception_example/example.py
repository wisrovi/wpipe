"""
Example: Retry with Custom Exception

Shows retry with custom exception handling.
"""

from typing import Any

from wpipe import Pipeline


class CustomError(Exception):
    """Custom error for retry demo."""
    pass


def failing_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that might fail."""
    return {"result": "success"}


def main() -> None:
    """Run retry with custom exception example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (failing_step, "Failing Step", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()