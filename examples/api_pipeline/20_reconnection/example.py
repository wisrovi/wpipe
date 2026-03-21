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

    def __init__(self):
        self.call_count = 0
        self.available_after = 2

    def should_fail(self):
        self.call_count += 1
        return self.call_count <= self.available_after


simulator = APIConnectionSimulator()


def process_data(data):
    """Processing function."""
    return {"result": data.get("value", 0) * 2, "attempts": simulator.call_count}


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "reconnect_token"}

    pipeline = Pipeline(
        worker_name="reconnect_worker", api_config=api_config, verbose=False
    )

    pipeline.set_steps([(process_data, "Process", "v1.0")])

    results = []
    for i in range(5):
        result = pipeline.run({"value": i + 1})
        results.append(result)
        time.sleep(0.1)

    for r in results:
        print(f"Result: {r['result']}, Attempts: {r['attempts']}")


if __name__ == "__main__":
    main()
