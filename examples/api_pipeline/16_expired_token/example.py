"""
16 Expired Token

Demonstrates handling of expired/invalid authentication tokens.
Pipeline should gracefully handle 401 Unauthorized responses.

What it evaluates:
- Token expiration handling
- 401 Unauthorized response handling
- Graceful fallback when auth fails
- Clear error messages for auth issues
"""

from wpipe import Pipeline


def process_data(data):
    """Simple processing function."""
    return {"result": data.get("value", 0) * 2, "status": "authenticated"}


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "expired_token_12345"}

    pipeline = Pipeline(
        worker_name="expired_token_worker", api_config=api_config, verbose=True
    )

    pipeline.set_steps([(process_data, "Process", "v1.0")])
    result = pipeline.run({"value": 10})
    print(f"Result: {result}")
    assert result["result"] == 20


if __name__ == "__main__":
    main()
