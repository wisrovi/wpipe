"""
API Pipeline Example

This example demonstrates how to use the Pipeline with API tracking.
When a worker_id is set and API config is provided, the pipeline
will track task execution via the API server.
"""

from wpipe.pipe import Pipeline


def process_data(data):
    """Process the input data."""
    value = data.get("value", 0)
    return {"processed": value * 2, "status": "success"}


def save_results(data):
    """Save the processing results."""
    return {"saved": True, "result": data.get("processed", 0)}


def main():
    """Run the API pipeline example."""
    api_config = {"base_url": "http://localhost:8418", "token": "your_token_here"}

    pipeline = Pipeline(
        worker_name="example_worker", api_config=api_config, verbose=True
    )

    pipeline.set_steps(
        [
            (process_data, "Process Data", "v1.0"),
            (save_results, "Save Results", "v1.0"),
        ]
    )

    worker_id = pipeline.worker_register("example_worker", "v1.0")

    if worker_id:
        print(f"Worker registered with ID: {worker_id}")
        pipeline.set_worker_id(worker_id.get("id"))

    result = pipeline.run({"value": 42})

    print(f"Pipeline result: {result}")


if __name__ == "__main__":
    main()
