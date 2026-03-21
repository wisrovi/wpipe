"""
02 Retry - Success After Retries

Shows a function that succeeds after a few failed attempts.
"""

from typing import Any

from wpipe import Pipeline


class FlakyStep:
    """A step that fails a specified number of times before succeeding."""

    def __init__(self, fail_count: int = 2) -> None:
        """Initializes the flaky step.

        Args:
            fail_count: Number of times to fail before succeeding.
        """
        self.attempts = 0
        self.fail_count = fail_count

    def __call__(self, data: dict[str, Any]) -> dict[str, Any]:
        """Executes the step, failing a specified number of times.

        Args:
            data: Pipeline data dictionary.

        Returns:
            Dictionary with success status and attempt count.

        Raises:
            ConnectionError: Until fail_count attempts have been made.
        """
        self.attempts += 1
        if self.attempts <= self.fail_count:
            raise ConnectionError(f"Attempt {self.attempts} failed")
        return {"success": True, "attempts": self.attempts}


def main() -> None:
    """Runs the success-after-retry example pipeline."""
    pipeline = Pipeline(max_retries=3, retry_delay=0.1, verbose=True)

    pipeline.set_steps(
        [
            (FlakyStep(fail_count=2), "Flaky Step", "v1.0"),
        ]
    )

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
