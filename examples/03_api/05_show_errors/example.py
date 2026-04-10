"""
05 API Pipeline - Show API Errors Flag

Shows how to use SHOW_API_ERRORS flag to raise API errors.
When enabled, API errors raise exceptions instead of being ignored.
"""

from wpipe import Pipeline


def process(data: dict) -> dict:
    """Simple processing function.

    Args:
        data: Dictionary with 'value' key.

    Returns:
        Dictionary with doubled 'result'.
    """
    return {"result": data["value"] * 2}


def main() -> None:
    """Run the SHOW_API_ERRORS example.

    Demonstrates:
        - SHOW_API_ERRORS flag controls exception behavior
        - When True, API errors raise exceptions
        - Pipeline can fail fast on API issues
    """
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
    }

    pipeline = Pipeline(
        worker_name="test_worker",
        api_config=api_config,
        verbose=True,
    )

    pipeline.SHOW_API_ERRORS = True

    pipeline.set_steps(
        [
            (process, "Process", "v1.0"),
        ]
    )

    try:
        pipeline.set_worker_id("worker_test12345")
        result = pipeline.run({"value": 10})
        print(f"Result: {result}")
    except Exception as e:
        print(f"API Error (expected): {e}")
        result = pipeline.run({"value": 10})
        print(f"Result (local): {result}")


if __name__ == "__main__":
    main()
