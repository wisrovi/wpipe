"""
07 API Pipeline - Retry Configuration

Shows configuring retry for failed API calls.
"""

from wpipe import Pipeline


def process(data):
    return {"result": "done"}


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "test_token"}

    pipeline = Pipeline(
        worker_name="retry_test", api_config=api_config, max_retries=3, verbose=True
    )

    pipeline.set_steps([(process, "Process", "v1.0")])
    result = pipeline.run({"value": 10})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
