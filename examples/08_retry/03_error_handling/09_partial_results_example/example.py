"""
Example: Error Handling - Partial Results

Shows storing partial results on error.
"""

from typing import Any

from wpipe import Pipeline


def step1(data: dict[str, Any]) -> dict[str, Any]:
    """Step 1 - stores partial."""
    return {"step1": "done", "partial": True}


def step2(data: dict[str, Any]) -> dict[str, Any]:
    """Step 2."""
    return {"step2": "done"}


def main() -> None:
    """Run partial results example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()