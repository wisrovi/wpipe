"""
08 API Pipeline - Custom Headers

Shows adding custom headers to API requests.
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
    """Run the custom headers example pipeline."""
    api_config: dict[str, str | dict[str, str]] = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
        "headers": {"X-Custom-Header": "value"},
    }

    pipeline = Pipeline(worker_name="headers_test", api_config=api_config, verbose=True)

    pipeline.set_steps([(process, "Process", "v1.0")])
    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
