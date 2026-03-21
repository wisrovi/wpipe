"""
Example: Pipeline with API Connection

This example demonstrates how to connect a pipeline to an external API
for tracking and monitoring pipeline execution.
"""

from wpipe.pipe import Pipeline
from wpipe.exception import TaskError


def data_validation(data: dict) -> dict:
    """Validate input data."""
    if "x" not in data:
        raise ValueError("Missing required field 'x'")
    return {"validated": True, "x": data["x"]}


def data_processing(data: dict) -> dict:
    """Process the validated data."""
    x = data["x"]
    return {"processed": True, "result": x * 100}


def data_transformation(data: dict) -> dict:
    """Transform the processed data."""
    result = data.get("result", 0)
    return {"transformed": True, "output": result / 10}


def final_aggregation(data: dict) -> dict:
    """Final aggregation step."""
    output = data.get("output", 0)
    return {"completed": True, "final_value": output}


def main():
    """Execute the pipeline with API connection."""
    api_config = {"base_url": "http://localhost:8418", "token": "mysecrettoken"}

    pipeline = Pipeline(
        worker_name="example_worker", api_config=api_config, verbose=True
    )

    pipeline.set_steps(
        [
            (data_validation, "Data Validation", "v1.0"),
            (data_processing, "Data Processing", "v1.0"),
            (data_transformation, "Data Transformation", "v1.0"),
            (final_aggregation, "Final Aggregation", "v1.0"),
        ]
    )

    worker_id = pipeline.worker_register(name="example_pipeline", version="v1.0.0")

    print(f"Registered worker: {worker_id}")

    pipeline.set_worker_id(worker_id.get("id"))

    try:
        result = pipeline.run({"x": 42})
        print(f"Pipeline result: {result}")

        assert "final_value" in result
        print("Pipeline executed successfully!")

    except TaskError as e:
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()
