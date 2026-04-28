"""
Example: Error Handling - Additional Example

Shows additional error handling patterns.
"""

from typing import Any

from wpipe import Pipeline


def final_step(data: dict[str, Any]) -> dict[str, Any]:
    """Final step."""
    return {"final": "done"}


def main() -> None:
    """Run additional example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (final_step, "Final Step", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()