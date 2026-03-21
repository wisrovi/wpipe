"""
02 API Pipeline - Worker ID Management

Shows how to set and track worker identity for API operations.
"""

from wpipe import Pipeline


def fetch_data(data: dict) -> dict:
    """Fetch data from a source.

    Args:
        data: Input dictionary.

    Returns:
        Dictionary with 'data' key containing a list of numbers.
    """
    return {"data": [1, 2, 3, 4, 5]}


def transform_data(data: dict) -> dict:
    """Transform data by multiplying each element.

    Args:
        data: Dictionary with 'data' key.

    Returns:
        Dictionary with 'transformed' key containing doubled values.
    """
    original: list[int] = data.get("data", [])
    transformed: list[int] = [x * 2 for x in original]
    return {"transformed": transformed}


def main() -> None:
    """Run the worker ID example.

    Demonstrates:
        - Setting worker_id manually
        - Tracking worker_id in pipeline
        - Enabling API communication
    """
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "test_token_abc12345",
    }

    pipeline = Pipeline(
        worker_name="transform_worker",
        api_config=api_config,
        verbose=True,
    )

    pipeline.set_steps(
        [
            (fetch_data, "Fetch Data", "v1.0"),
            (transform_data, "Transform Data", "v1.0"),
        ]
    )

    try:
        pipeline.set_worker_id("worker_abc12345")
        result = pipeline.run({})
        print(f"Result: {result}")
    except Exception as e:
        print(f"API not available: {e}")
        result = pipeline.run({})
        print(f"Result (local): {result}")


if __name__ == "__main__":
    main()
