"""
02 API Pipeline - Worker ID Management

Shows how to set and manage worker IDs.
"""

from wpipe import Pipeline


def fetch_data(data):
    return {"data": [1, 2, 3, 4, 5]}


def transform_data(data):
    return {"transformed": [x * 2 for x in data["data"]]}


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "test_token"}

    pipeline = Pipeline(
        worker_name="transform_worker", api_config=api_config, verbose=True
    )

    pipeline.set_steps(
        [
            (fetch_data, "Fetch Data", "v1.0"),
            (transform_data, "Transform Data", "v1.0"),
        ]
    )

    worker_id_str = "worker_abc12345"
    pipeline.set_worker_id(worker_id_str)

    print(f"Worker ID set to: {pipeline.worker_id}")
    print(f"Send to API: {pipeline.send_to_api}")

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
