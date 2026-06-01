"""
Example: Error Handling - Error in Recovery

Shows error in recovery handler.
"""

from typing import Any

from wpipe import Pipeline


def main_step(data: dict[str, Any]) -> dict[str, Any]:
    """Main step."""
    return {"main": "done"}


def recovery_handler(data: dict[str, Any]) -> dict[str, Any]:
    """Recovery handler."""
    return {"recovery": "success"}


def main() -> None:
    """Run error in recovery example."""
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (main_step, "Main", "v1.0"),
        (recovery_handler, "Recovery", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()