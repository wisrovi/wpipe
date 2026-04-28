"""
Example: Error Handling - Middle Step Error

Shows error in middle of pipeline.
"""

from typing import Any

from wpipe import Pipeline


def step1(data: dict[str, Any]) -> dict[str, Any]:
    """First step."""
    return {"step1": "done"}


def step2(data: dict[str, Any]) -> dict[str, Any]:
    """Second step - fails."""
    if data.get("fail"):
        raise RuntimeError("Middle step failed!")
    return {"step2": "done"}


def step3(data: dict[str, Any]) -> dict[str, Any]:
    """Third step."""
    return {"step3": "done"}


def main() -> None:
    """Run middle error example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (step1, "Step 1", "v1.0"),
        (step2, "Step 2", "v1.0"),
        (step3, "Step 3", "v1.0"),
    ])

    result = pipeline.run({"fail": False})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()