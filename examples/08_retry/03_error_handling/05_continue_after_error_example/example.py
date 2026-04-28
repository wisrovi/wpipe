"""
Example: Error Handling - Continue After Error

Shows continuing pipeline after error occurs.
"""

from typing import Any

from wpipe import Pipeline


def initial_step(data: dict[str, Any]) -> dict[str, Any]:
    """Initial step."""
    return {"init": "done"}


def recovery_step(data: dict[str, Any]) -> dict[str, Any]:
    """Recovery step."""
    return {"recovery": "success"}


def main() -> None:
    """Run continue after error example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (initial_step, "Initial", "v1.0"),
        (recovery_step, "Recovery", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()