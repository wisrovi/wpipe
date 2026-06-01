"""
Example: For Loop - Break on Error

Shows For loop that handles errors.
"""

from typing import Any

from wpipe import For, Pipeline, step


@step(name="may_fail", version="v1.0")
def may_fail(data: dict[str, Any]) -> dict[str, Any]:
    """Step that might fail but continues."""
    counter = data.get("counter", 0) + 1
    data["counter"] = counter
    return data


def main() -> None:
    """Run break on error example."""
    pipeline = Pipeline(pipeline_name="break_on_error", verbose=False)

    pipeline.set_steps([
        (lambda d: {"counter": 0}, "init", "v1"),
        For(iterations=3, steps=[may_fail]),
    ])

    result = pipeline.run({})
    print(f"Counter: {result.get('counter')}")
    print("Test passed!")


if __name__ == "__main__":
    main()