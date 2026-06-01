"""
Example: Dashboard - Complete Example

Shows complete dashboard features.
"""

from typing import Any

from wpipe import Pipeline, step


@step(name="process", version="v1.0")
def process_step(data: dict[str, Any]) -> dict[str, Any]:
    """Process step."""
    return {"result": "processed", "value": 100}


def main() -> None:
    """Run complete dashboard example."""
    pipeline = Pipeline(
        pipeline_name="complete_demo",
        verbose=True,
    )

    pipeline.set_steps([
        (process_step, "Process", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result: {result['result']}")


if __name__ == "__main__":
    main()