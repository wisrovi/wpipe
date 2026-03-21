"""
Basic Pipeline - Pipeline Configuration

Using pipeline configuration for reusable setups.
"""

from typing import Any

from wpipe import Pipeline


def create_configured_pipeline(extra_steps: list | None = None) -> Pipeline:
    """Create a configured pipeline with optional extra steps.

    Args:
        extra_steps: Additional steps to add to pipeline.

    Returns:
        Configured Pipeline instance.
    """
    pipeline = Pipeline(verbose=True)

    base_steps: list[tuple[Any, str, str]] = [
        (lambda d: {"v1": d.get("value", 0)}, "Base Step", "v1.0"),
    ]

    if extra_steps:
        base_steps.extend(extra_steps)

    pipeline.set_steps(base_steps)
    return pipeline


def main() -> None:
    """Run the pipeline configuration example.

    Demonstrates:
        - Creating reusable pipeline configurations
        - Adding extra steps dynamically
        - Cloning and extending pipelines
    """
    p1 = create_configured_pipeline()
    r1 = p1.run({"value": 10})
    print(f"Basic: {r1}")

    extra = [(lambda d: {"v2": d.get("v1", 0) * 2}, "Extra", "v1.0")]
    p2 = create_configured_pipeline(extra)
    r2 = p2.run({"value": 10})
    print(f"Extended: {r2}")


if __name__ == "__main__":
    main()
