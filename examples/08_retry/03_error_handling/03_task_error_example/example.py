"""
Example: Error Handling - Task Validation

Shows task validation with proper error handling.
"""

from typing import Any

from wpipe import Pipeline, step


@step(name="validate", version="v1.0")
def validate_input(data: dict[str, Any]) -> dict[str, Any]:
    """Validate input data."""
    value = data.get("value", 0)
    if value < 0:
        raise ValueError("Value must be positive")
    return {"validated": value, "status": "valid"}


def main() -> None:
    """Run task validation example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (validate_input, "Validate Input", "v1.0"),
    ])

    result = pipeline.run({"value": 10})
    print(f"Validated: {result['validated']}")


if __name__ == "__main__":
    main()