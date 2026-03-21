"""
06 API Pipeline - Full Configuration

Shows full API configuration with all options.
"""

from wpipe import Pipeline


def process(data):
    return {"result": data["value"] * 2}


def main():
    api_config = {
        "base_url": "http://localhost:8418",
        "token": "test_token",
        "timeout": 30,
        "retry": 3,
    }

    pipeline = Pipeline(worker_name="full_config", api_config=api_config, verbose=True)

    pipeline.set_steps([(process, "Process", "v1.0")])
    result = pipeline.run({"value": 10})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
