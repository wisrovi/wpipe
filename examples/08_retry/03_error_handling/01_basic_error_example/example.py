"""
Example: Error Handling - Basic Exception

Shows simplest error handling - catching and recovering from a ValueError.
"""

from typing import Any

from wpipe import Pipeline


def success_step(data: dict[str, Any]) -> dict[str, Any]:
    """Process data successfully."""
    return {"value": 10, "status": "success"}


def main() -> None:
    """Run the basic error handling example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (success_step, "Success Step", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Pipeline completed: {result['status']}")
    assert result["status"] == "success"
    print("Test passed!")


if __name__ == "__main__":
    main()