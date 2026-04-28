"""
Example: Dashboard - Alerts

Shows alert system basic usage.
"""

from typing import Any

from wpipe import Pipeline


def slow_step(data: dict[str, Any]) -> dict[str, Any]:
    """Step that takes time."""
    return {"result": "done"}


def main() -> None:
    """Run alerts example."""
    pipeline = Pipeline(pipeline_name="alerts_demo", verbose=True)

    pipeline.set_steps([
        (slow_step, "Slow Step", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()