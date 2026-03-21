"""
01 API Pipeline - Basic API Configuration

Shows how to configure a pipeline with API settings.
Note: Requires an API server running at the configured URL.
"""

from wpipe import Pipeline


def process(data):
    return {"result": data["value"] * 2, "status": "success"}


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "test_token_123"}

    pipeline = Pipeline(worker_name="demo_worker", api_config=api_config, verbose=True)

    pipeline.set_steps(
        [
            (process, "Process Data", "v1.0"),
        ]
    )

    try:
        worker_id = pipeline.worker_register("demo_worker", "v1.0")
        if worker_id:
            print(f"Worker registered: {worker_id}")
            pipeline.set_worker_id(worker_id.get("id"))
        result = pipeline.run({"value": 42})
        print(f"Result: {result}")
    except Exception as e:
        print(f"API not available: {e}")
        result = pipeline.run({"value": 42})
        print(f"Result (local): {result}")


if __name__ == "__main__":
    main()
