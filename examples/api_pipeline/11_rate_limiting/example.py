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

request_times = []
RATE_LIMIT = 5
WINDOW_SIZE = 2


def check_rate_limit(data):
    """Check if request is within rate limit."""
    current_time = time.time()
    request_times.append(current_time)
    times_in_window = [t for t in request_times if current_time - t < WINDOW_SIZE]
    request_times[:] = times_in_window

    within_limit = len(times_in_window) <= RATE_LIMIT
    return {"allowed": within_limit, "requests_in_window": len(times_in_window)}


def process_request(data):
    """Process the request."""
    return {"processed": True, "request_id": data.get("request_id", "default")}


def log_request(data):
    """Log the processed request."""
    return {"logged": True, "request_id": data.get("request_id")}


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "rate_limit_token"}

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

    results = []
    for i in range(3):
        result = pipeline.run({"request_id": f"req_{i}"})
        results.append(result)

    print(f"Results: {results}")
    assert all(r["processed"] for r in results)


if __name__ == "__main__":
    main()
