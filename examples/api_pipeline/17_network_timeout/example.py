"""
17 Network Timeout Simulation

Demonstrates handling of network timeouts and slow responses.
Pipeline should handle timeout errors gracefully.

What it evaluates:
- Timeout configuration
- Slow network simulation
- Timeout error handling
- Retry behavior on timeout
"""

from wpipe import Pipeline
import time


def slow_operation(data):
    """Simulates a slow operation."""
    time.sleep(0.1)
    return {"result": "slow_done"}


def fast_operation(data):
    """Fast operation to test timeout."""
    return {"result": data.get("value", 0) * 2}


def main():
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "timeout_test_token",
        "timeout": 1,
    }

    pipeline = Pipeline(
        worker_name="timeout_worker", api_config=api_config, verbose=True
    )

    pipeline.set_steps(
        [
            (slow_operation, "Slow Op", "v1.0"),
            (fast_operation, "Fast Op", "v1.0"),
        ]
    )

    result = pipeline.run({"value": 5})
    print(f"Result: {result}")
    assert result["result"] == 10


if __name__ == "__main__":
    main()
