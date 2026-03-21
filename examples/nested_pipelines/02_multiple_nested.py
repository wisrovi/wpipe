"""
02 Nested Pipelines - Multiple Nested Pipelines

Shows running multiple nested pipelines in sequence.
"""

from wpipe import Pipeline


def pipeline_a_step1(data):
    return {"a1": 1}


def pipeline_a_step2(data):
    return {"a2": 2}


def pipeline_b_step1(data):
    return {"b1": 10}


def pipeline_b_step2(data):
    return {"b2": 20}


def final_step(data):
    return {"final": data.get("a1", 0) + data.get("b1", 0)}


def main():
    pipeline_a = Pipeline(verbose=False)
    pipeline_a.set_steps(
        [
            (pipeline_a_step1, "A Step 1", "v1.0"),
            (pipeline_a_step2, "A Step 2", "v1.0"),
        ]
    )

    pipeline_b = Pipeline(verbose=False)
    pipeline_b.set_steps(
        [
            (pipeline_b_step1, "B Step 1", "v1.0"),
            (pipeline_b_step2, "B Step 2", "v1.0"),
        ]
    )

    main_pipeline = Pipeline(verbose=True)
    main_pipeline.set_steps(
        [
            (pipeline_a.run, "Pipeline A", "v1.0"),
            (pipeline_b.run, "Pipeline B", "v1.0"),
            (final_step, "Final Step", "v1.0"),
        ]
    )

    result = main_pipeline.run({})

    print(f"Result: {result}")
    assert result["a1"] == 1
    assert result["a2"] == 2
    assert result["b1"] == 10
    assert result["b2"] == 20
    assert result["final"] == 11


if __name__ == "__main__":
    main()
