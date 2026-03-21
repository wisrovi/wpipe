"""
01 Retry - Basic Retry on Failure

The simplest retry example - retry when a function fails.
"""

from typing import Any

from wpipe import Pipeline


def unreliable_step(data: dict[str, Any]) -> None:
    """Simulates a step that always fails with a network error.

    Args:
        data: Pipeline data dictionary.

    Raises:
        ConnectionError: Always raised to simulate a network failure.
    """
    raise ConnectionError("Network error!")


def recovery_step(data: dict[str, Any]) -> dict[str, str]:
    """Simulates a recovery step after retry failure.

    Args:
        data: Pipeline data dictionary.

    Returns:
        Dictionary with recovery status.
    """
    return {"status": "recovered"}


def main() -> None:
    """Runs the basic retry example pipeline."""
    pipeline = Pipeline(max_retries=3, retry_delay=0.1, verbose=True)

    pipeline.set_steps(
        [
            (unreliable_step, "Unreliable Step", "v1.0"),
        ]
    )

    try:
        result = pipeline.run({})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed after retries: {e}")


if __name__ == "__main__":
    main()
