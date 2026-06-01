"""
Example: Dashboard - Performance Comparison

Shows pipeline performance comparison.
"""

from typing import Any

from wpipe import Pipeline


def fast_step(data: dict[str, Any]) -> dict[str, Any]:
    """Fast step."""
    return {"value": 100}


def slow_step(data: dict[str, Any]) -> dict[str, Any]:
    """Slow step."""
    return {"value": 50}


def main() -> None:
    """Run performance comparison example."""
    p1 = Pipeline(pipeline_name="fast_pipeline", verbose=False)
    p1.set_steps([(fast_step, "Fast", "v1.0")])
    result1 = p1.run({})

    p2 = Pipeline(pipeline_name="slow_pipeline", verbose=False)
    p2.set_steps([(slow_step, "Slow", "v1.0")])
    result2 = p2.run({})

    print(f"Fast: {result1.get('value')}")
    print(f"Slow: {result2.get('value')}")


if __name__ == "__main__":
    main()