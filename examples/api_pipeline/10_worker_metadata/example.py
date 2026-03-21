"""
10 API Pipeline - Worker Metadata

Shows passing custom metadata to worker registration.
"""

from wpipe import Pipeline


def process(data: dict) -> dict:
    """Process input data.

    Args:
        data: Input dictionary.

    Returns:
        Dictionary with result and worker info.
    """
    return {"result": "done", "worker": "metadata_test"}


def main() -> None:
    """Run the worker metadata example.

    Demonstrates:
        - worker_metadata parameter in api_config
        - Metadata sent during worker registration
    """
    api_config: dict[str, str | dict] = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
        "worker_metadata": {"version": "1.0", "environment": "test"},
    }

    pipeline = Pipeline(
        worker_name="metadata_test",
        api_config=api_config,
        verbose=True,
    )

    pipeline.set_steps([(process, "Process", "v1.0")])

    try:
        result = pipeline.run({})
        print(f"Result: {result}")
    except Exception as e:
        print(f"API Error: {e}")
        result = pipeline.run({})
        print(f"Result (local): {result}")


if __name__ == "__main__":
    main()
