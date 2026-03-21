"""
06 API Pipeline - Timeout Configuration

Shows configuring timeout for API calls.
"""

from wpipe import Pipeline


def process(data: dict) -> dict:
    """Process input data.

    Args:
        data: Dictionary with 'value' key.

    Returns:
        Dictionary with doubled 'result'.
    """
    return {"result": data["value"] * 2}


def main() -> None:
    """Run the timeout example.

    Demonstrates:
        - Timeout configuration in api_config
        - API calls respect timeout settings
    """
    api_config: dict[str, str | int] = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
        "timeout": 30,
    }

    pipeline = Pipeline(
        worker_name="timeout_test",
        api_config=api_config,
        verbose=True,
    )

    pipeline.set_steps([(process, "Process", "v1.0")])

    try:
        result = pipeline.run({"value": 10})
        print(f"Result: {result}")
    except Exception as e:
        print(f"API Error: {e}")
        result = pipeline.run({"value": 10})
        print(f"Result (local): {result}")


if __name__ == "__main__":
    main()
