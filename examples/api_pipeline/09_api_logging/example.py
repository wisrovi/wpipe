"""
09 API Pipeline - Logging Configuration

Shows configuring logging for API calls.
"""

from wpipe import Pipeline


def process(data: dict) -> dict:
    """Process data through the pipeline.

    Args:
        data: Input data dictionary to process.

    Returns:
        Dictionary with processing result.

    Example:
        >>> process({})
        {'result': 'done'}
    """
    return {"result": "done"}


def main() -> None:
    """Run the logging configuration example pipeline."""
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
    }

    pipeline = Pipeline(worker_name="logging_test", api_config=api_config, verbose=True)

    pipeline.set_steps([(process, "Process", "v1.0")])
    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
