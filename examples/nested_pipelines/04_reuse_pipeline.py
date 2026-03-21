"""
04 Nested Pipelines - Reusing Pipeline Objects

Shows how to reuse the same pipeline object multiple times.
"""

from wpipe import Pipeline


def process_item(data):
    item = data.get("item", 0)
    return {"processed": item * 2}


def main():
    reusable_pipeline = Pipeline(verbose=False)
    reusable_pipeline.set_steps(
        [
            (process_item, "Process Item", "v1.0"),
        ]
    )

    main_pipeline = Pipeline(verbose=True)
    main_pipeline.set_steps(
        [
            (reusable_pipeline.run, "Process 1", "v1.0"),
            (reusable_pipeline.run, "Process 2", "v1.0"),
            (reusable_pipeline.run, "Process 3", "v1.0"),
        ]
    )

    result = main_pipeline.run({"item": 10})

    print(f"Result: {result}")
    assert result["processed"] == 20


if __name__ == "__main__":
    main()
