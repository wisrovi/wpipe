"""
05 API Pipeline - Show API Errors Flag

Shows how to use the SHOW_API_ERRORS flag to raise API errors.
"""

from wpipe import Pipeline


def process(data):
    return {"result": data["value"] * 2}


def main():
    api_config = {"base_url": "http://localhost:8418", "token": "test_token"}

    pipeline = Pipeline(worker_name="test_worker", api_config=api_config, verbose=True)

    pipeline.SHOW_API_ERRORS = True
    pipeline.set_worker_id("worker_test12345")

    pipeline.set_steps(
        [
            (process, "Process", "v1.0"),
        ]
    )

    result = pipeline.run({"value": 10})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
