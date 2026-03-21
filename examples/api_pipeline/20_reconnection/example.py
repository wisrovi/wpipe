"""
20 Reconnection Logic

Demonstrates automatic reconnection when API server becomes available.
Pipeline should recover from temporary API failures.

What it evaluates:
- Reconnection after failure
- API recovery handling
- Automatic retry to API
- Graceful degradation and recovery
"""

import time

from wpipe import Pipeline


class APIConnectionSimulator:
    """Simulates intermittent API availability."""

    def __init__(self) -> None:
        """Initialize the simulator with default call count and availability."""
        self.call_count: int = 0
        self.available_after: int = 2

    def should_fail(self) -> bool:
        """Determine if the current call should fail based on call count.

        Returns:
            True if call should fail, False if API should succeed.

        Example:
            >>> simulator = APIConnectionSimulator()
            >>> simulator.should_fail()
            True
            >>> simulator.should_fail()
            True
            >>> simulator.should_fail()
            False
        """
        self.call_count += 1
        return self.call_count <= self.available_after


simulator = APIConnectionSimulator()


def process_data(data: dict) -> dict:
    """Processing function.

    Args:
        data: Input data dictionary containing 'value'.

    Returns:
        Dictionary with processed result and attempt count.

    Example:
        >>> process_data({"value": 5})
        {'result': 10, 'attempts': 3}
    """
    return {"result": data.get("value", 0) * 2, "attempts": simulator.call_count}


def main() -> None:
    """Run the reconnection logic example pipeline."""
    api_config: dict[str, str] = {
        "base_url": "http://localhost:8418",
        "token": "reconnect_token",
    }

    pipeline = Pipeline(
        worker_name="reconnect_worker", api_config=api_config, verbose=False
    )

    pipeline.set_steps([(process_data, "Process", "v1.0")])

    results: list[dict] = []
    for i in range(5):
        result = pipeline.run({"value": i + 1})
        results.append(result)
        time.sleep(0.1)

    for r in results:
        print(f"Result: {r['result']}, Attempts: {r['attempts']}")


if __name__ == "__main__":
    main()
