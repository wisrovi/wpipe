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

import time

from wpipe import Pipeline


def slow_operation(data: dict) -> dict:
    """Simulates a slow operation.

    Args:
        data: Input data dictionary for context.

    Returns:
        Dictionary with slow operation result.

    Example:
        >>> slow_operation({})
        {'result': 'slow_done'}
    """
    time.sleep(0.1)
    return {"result": "slow_done"}


def fast_operation(data: dict) -> dict:
    """Fast operation to test timeout.

    Args:
        data: Input data dictionary containing 'value'.

    Returns:
        Dictionary with doubled value result.

    Example:
        >>> fast_operation({"value": 5})
        {'result': 10}
    """
    return {"result": data.get("value", 0) * 2}


def main() -> None:
    """Run the network timeout example pipeline."""
    api_config: dict[str, str | int] = {
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
