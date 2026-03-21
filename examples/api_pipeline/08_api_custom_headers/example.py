"""
08 API Pipeline - Custom Headers

Shows adding custom headers to API requests.
"""

from wpipe import Pipeline

def process(data):
    return {"result": "done"}

def main():
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
        "headers": {"X-Custom-Header": "value"}
    }

    pipeline = Pipeline(
        worker_name="headers_test",
        api_config=api_config,
        verbose=True
    )

    pipeline.set_steps([(process, "Process", "v1.0")])
    result = pipeline.run({})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
