"""
18 Invalid URL

Demonstrates handling of invalid/malformed URLs in API configuration.
Pipeline should handle URL validation errors gracefully.

What it evaluates:
- Invalid URL handling
- Malformed URL detection
- Clear error messages
- Fallback to local execution
"""

from wpipe import Pipeline


def process_data(data: dict) -> dict:
    """Simple processing function.

    Args:
        data: Input data dictionary containing 'value'.

    Returns:
        Dictionary with doubled value result.

    Example:
        >>> process_data({"value": 5})
        {'result': 10}
    """
    return {"result": data.get("value", 0) * 2}


def main() -> None:
    """Run the invalid URL example pipeline."""
    invalid_urls: list[str] = [
        "not-a-url",
        "http://",
        "://missing-protocol.com",
        "http:/invalid",
    ]

    for url in invalid_urls:
        api_config: dict[str, str] = {"base_url": url, "token": "test_token"}

        pipeline = Pipeline(
            worker_name="invalid_url_worker", api_config=api_config, verbose=False
        )

        pipeline.set_steps([(process_data, "Process", "v1.0")])
        result = pipeline.run({"value": 5})
        print(f"URL: {url} -> Result: {result['result']}")


if __name__ == "__main__":
    main()
