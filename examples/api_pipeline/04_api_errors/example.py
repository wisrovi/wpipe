"""
04 API Pipeline - API Error Handling

Shows how API errors are handled when server is unavailable.
Pipeline continues executing even if API calls fail.
"""

from wpipe import Pipeline


def fetch_from_api(data: dict) -> dict:
    """Simulate fetching data from API.

    Args:
        data: Input dictionary.

    Returns:
        Dictionary with 'data' key.
    """
    return {"data": "fetched from API"}


def process_data(data: dict) -> dict:
    """Process data from API response.

    Args:
        data: Dictionary with 'data' key.

    Returns:
        Dictionary with 'result' and 'source' keys.
    """
    return {"result": "processed", "source": data.get("data")}


def main() -> None:
    """Run the error handling example.

    Demonstrates:
        - API errors don't stop pipeline
        - Invalid API server handled gracefully
        - Local execution continues
    """
    api_config: dict[str, str] = {
        "base_url": "http://invalid-host:9999",
        "token": "invalid_token",
    }

    pipeline = Pipeline(
        worker_name="test_worker",
        api_config=api_config,
        verbose=True,
    )

    pipeline.set_steps(
        [
            (fetch_from_api, "Fetch from API", "v1.0"),
            (process_data, "Process Data", "v1.0"),
        ]
    )

    try:
        pipeline.set_worker_id("worker_test12345")
        result = pipeline.run({})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        result = pipeline.run({})
        print(f"Result (local): {result}")


if __name__ == "__main__":
    main()
