"""
Example: Error Handling - Filter Exceptions

Shows filtering which exceptions to retry.
"""

from typing import Any

from wpipe import Pipeline


def unreliable_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that might fail."""
    return {"result": "success"}


def main() -> None:
    """Run filter exceptions example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (unreliable_step, "Unreliable Step", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()