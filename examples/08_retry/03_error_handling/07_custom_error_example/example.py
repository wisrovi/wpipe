"""
Example: Error Handling - Custom Error

Shows custom error handling.
"""

from typing import Any

from wpipe import Pipeline


def process_data(data: dict[str, Any]) -> dict[str, Any]:
    """Process data successfully."""
    return {"result": "success"}


def main() -> None:
    """Run custom error example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (process_data, "Process", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()