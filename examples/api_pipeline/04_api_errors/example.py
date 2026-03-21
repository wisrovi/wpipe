"""
04 API Pipeline - API Error Handling

Shows how API errors are handled when the server is unavailable.
"""

from wpipe import Pipeline


def fetch_from_api(data):
    return {"data": "fetched from API"}


def process_data(data):
    return {"result": "processed", "source": data.get("data")}


def main():
    api_config = {"base_url": "http://invalid-host:9999", "token": "invalid_token"}

    pipeline = Pipeline(worker_name="test_worker", api_config=api_config, verbose=True)

    pipeline.set_steps(
        [
            (fetch_from_api, "Fetch from API", "v1.0"),
            (process_data, "Process Data", "v1.0"),
        ]
    )

    pipeline.set_worker_id("worker_test12345")

    result = pipeline.run({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
