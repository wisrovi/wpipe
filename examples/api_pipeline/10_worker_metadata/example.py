"""
10 Worker Metadata

Demonstrates passing custom metadata to the worker registration.
Metadata can include version info, environment, tags, etc.

What it evaluates:
- worker_metadata parameter in api_config
- Metadata is sent during worker registration
- Pipeline can track worker properties
"""

from wpipe import Pipeline


def process(data):
    """Simple processing function."""
    return {"result": "done", "worker": "metadata_test"}


def main():
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
        "worker_metadata": {"version": "1.0", "environment": "test"},
    }

    pipeline = Pipeline(
        worker_name="metadata_test", api_config=api_config, verbose=True
    )

    pipeline.set_steps([(process, "Process", "v1.0")])
    result = pipeline.run({})
    print(f"Result: {result}")
    assert result["result"] == "done"


if __name__ == "__main__":
    main()
