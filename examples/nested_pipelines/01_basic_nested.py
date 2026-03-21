"""
01 Nested Pipelines - Basic Nested Pipeline

The simplest nested pipeline example - one pipeline inside another.
"""

from wpipe import Pipeline


def inner_step1(data):
    return {"inner1": "done"}


def inner_step2(data):
    return {"inner2": "done"}


def outer_step(data):
    return {"outer": "done"}


def main():
    inner_pipeline = Pipeline(verbose=False)
    inner_pipeline.set_steps(
        [
            (inner_step1, "Inner Step 1", "v1.0"),
            (inner_step2, "Inner Step 2", "v1.0"),
        ]
    )

    outer_pipeline = Pipeline(verbose=True)
    outer_pipeline.set_steps(
        [
            (inner_pipeline.run, "Inner Pipeline", "v1.0"),
            (outer_step, "Outer Step", "v1.0"),
        ]
    )

    result = outer_pipeline.run({})

    print(f"Result: {result}")
    assert "inner1" in result
    assert "inner2" in result
    assert "outer" in result


if __name__ == "__main__":
    main()
