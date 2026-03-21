"""
11 Rate Limiting

Demonstrates implementing rate limiting in pipeline API calls.
Protects external services from being overwhelmed.

What it evaluates:
- Rate limiting configuration
- Request throttling
- API quota management
"""

import time

from wpipe import Pipeline

request_times: list[float] = []
RATE_LIMIT: int = 5
WINDOW_SIZE: int = 2


def check_rate_limit(data: dict) -> dict:
    """Check if request is within rate limit.

    Args:
        data: Input data dictionary containing optional request context.

    Returns:
        Dictionary with rate limit status and count of requests in window.

    Example:
        >>> check_rate_limit({})
        {'allowed': True, 'requests_in_window': 1}
    """
    current_time: float = time.time()
    request_times.append(current_time)
    times_in_window: list[float] = [
        t for t in request_times if current_time - t < WINDOW_SIZE
    ]
    request_times[:] = times_in_window

    within_limit: bool = len(times_in_window) <= RATE_LIMIT
    return {"allowed": within_limit, "requests_in_window": len(times_in_window)}


def process_request(data: dict) -> dict:
    """Process the request.

    Args:
        data: Input data dictionary containing request_id.

    Returns:
        Dictionary with processing status and request_id.

    Example:
        >>> process_request({"request_id": "req_1"})
        {'processed': True, 'request_id': 'req_1'}
    """
    return {"processed": True, "request_id": data.get("request_id", "default")}


def log_request(data: dict) -> dict:
    """Log the processed request.

    Args:
        data: Input data dictionary containing request_id.

    Returns:
        Dictionary with logging status and request_id.

    Example:
        >>> log_request({"request_id": "req_1"})
        {'logged': True, 'request_id': 'req_1'}
    """
    return {"logged": True, "request_id": data.get("request_id")}


def main() -> None:
    """Run the rate limiting example pipeline."""
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "rate_limit_token",
    }

    pipeline = Pipeline(
        worker_name="rate_limit_worker", api_config=api_config, verbose=True
    )

    pipeline.set_steps(
        [
            (check_rate_limit, "Check Rate Limit", "v1.0"),
            (process_request, "Process", "v1.0"),
            (log_request, "Log", "v1.0"),
        ]
    )

    results: list[dict] = []
    for i in range(3):
        result = pipeline.run({"request_id": f"req_{i}"})
        results.append(result)

    print(f"Results: {results}")
    assert all(r["processed"] for r in results)


if __name__ == "__main__":
    main()
