"""
03 Nested Pipelines - Data Passing Between Nested Pipelines

Shows how data is passed between nested pipelines.
"""

from wpipe import Pipeline


def generate_data(data):
    return {"value": 100}


def transform_data(data):
    return {"transformed": data.get("value", 0) * 2}


def combine_data(data):
    return {"combined": data.get("value", 0) + data.get("transformed", 0)}


def main():
    gen_pipeline = Pipeline(verbose=False)
    gen_pipeline.set_steps(
        [
            (generate_data, "Generate", "v1.0"),
        ]
    )

    transform_pipeline = Pipeline(verbose=False)
    transform_pipeline.set_steps(
        [
            (transform_data, "Transform", "v1.0"),
        ]
    )

    main_pipeline = Pipeline(verbose=True)
    main_pipeline.set_steps(
        [
            (gen_pipeline.run, "Generate Pipeline", "v1.0"),
            (transform_pipeline.run, "Transform Pipeline", "v1.0"),
            (combine_data, "Combine", "v1.0"),
        ]
    )

    result = main_pipeline.run({})

    print(f"Result: {result}")
    assert result["value"] == 100
    assert result["transformed"] == 200
    assert result["combined"] == 300


if __name__ == "__main__":
    main()
