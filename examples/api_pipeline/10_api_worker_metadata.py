"""
10 API Pipeline - Worker Metadata

Shows passing worker metadata to API.
"""

from wpipe import Pipeline

def process(data):
    return {"result": "done"}

def main():
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
        "worker_metadata": {"version": "1.0", "environment": "test"}
    }

    pipeline = Pipeline(
        worker_name="metadata_test",
        api_config=api_config,
        verbose=True
    )

    pipeline.set_steps([(process, "Process", "v1.0")])
    result = pipeline.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
