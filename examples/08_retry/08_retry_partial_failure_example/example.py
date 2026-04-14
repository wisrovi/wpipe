"""
08 Retry - Partial Pipeline Failure

Shows retry behavior when some steps fail.
"""

from typing import Any

from wpipe import Pipeline


def step1(data: dict[str, Any]) -> dict[str, str]:
    """First step that completes successfully.

    Args:
        data: Pipeline data dictionary.

    Returns:
        Dictionary with step1 completion status.
    """
    return {"step1": "done"}


def step2(data: dict[str, Any]) -> None:
    """Second step that always fails.

    Args:
        data: Pipeline data dictionary.

    Raises:
        ConnectionError: Always raised to simulate network error.
    """
    raise ConnectionError("Network error")


def step3(data: dict[str, Any]) -> dict[str, str]:
    """Third step that would complete successfully.

    Args:
        data: Pipeline data dictionary.

    Returns:
        Dictionary with step3 completion status.
    """
    return {"step3": "done"}


def main() -> None:
    """Runs the partial failure example demonstrating selective step retries."""
    pipeline = Pipeline(
        max_retries=2,
        retry_delay=0.1,
        verbose=True,
    )

    pipeline.set_steps(
        [
            (step1, "Step 1", "v1.0"),
            (step2, "Step 2", "v1.0"),
            (step3, "Step 3", "v1.0"),
        ]
    )

    try:
        _ = pipeline.run({})
    except Exception as e:
        print(f"Pipeline failed: {type(e).__name__}")


if __name__ == "__main__":
    main()
