"""
Example: Nested Pipelines

This example demonstrates how to nest pipelines within each other,
allowing for complex workflow compositions.
"""

from wpipe.pipe import Pipeline


def preprocess_data(data: dict) -> dict:
    """Preprocess the input data."""
    return {"preprocessed": True, "data": data.get("raw_data", "default")}


def process_batch(data: dict) -> dict:
    """Process a batch of data."""
    return {"batch_processed": True, "batch_size": 100}


def aggregate_results(data: dict) -> dict:
    """Aggregate processing results."""
    return {"aggregated": True, "total": 500}


def postprocess_final(data: dict) -> dict:
    """Final postprocessing step."""
    return {"postprocessed": True, "ready": True}


def main():
    """Demonstrate nested pipeline execution."""
    pipeline1 = Pipeline(verbose=False)
    pipeline1.set_steps(
        [
            (preprocess_data, "Preprocess", "v1.0"),
            (process_batch, "Process Batch", "v1.0"),
        ]
    )

    pipeline2 = Pipeline(verbose=False)
    pipeline2.set_steps(
        [
            (pipeline1.run, "Nested Pipeline 1", "v1.0"),
            (aggregate_results, "Aggregate", "v1.0"),
        ]
    )

    pipeline3 = Pipeline(verbose=True)
    pipeline3.set_steps(
        [
            (pipeline1.run, "Nested Pipeline 1", "v1.0"),
            (pipeline2.run, "Nested Pipeline 2", "v1.0"),
            (postprocess_final, "Postprocess", "v1.0"),
        ]
    )

    result = pipeline3.run({"raw_data": "test_input"})
    print(f"Final result: {result}")

    assert "preprocessed" in result
    assert "batch_processed" in result
    assert "aggregated" in result
    assert "postprocessed" in result

    print("All nested pipelines executed successfully!")


if __name__ == "__main__":
    main()
