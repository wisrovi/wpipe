"""
07 API Pipeline - Retry Configuration

Shows configuring retry for failed API calls.
"""

from wpipe import Pipeline


def process(data: dict) -> dict:
    """Process data through the pipeline.

    Args:
        data: Input data dictionary to process.

    Returns:
        Dictionary with processing result.

    Example:
        >>> process({"value": 10})
        {'result': 'done'}
    """
    return {"result": "done"}


def main() -> None:
    """Run the retry configuration example pipeline."""
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
    }

    pipeline = Pipeline(
        worker_name="retry_test", api_config=api_config, max_retries=3, verbose=True
    )

    pipeline.set_steps([(process, "Process", "v1.0")])
    result = pipeline.run({"value": 10})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
