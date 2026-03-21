"""
Basic Pipeline - Pipeline Chaining

Chaining multiple pipelines together.
"""

from wpipe import Pipeline


def pipeline_a():
    p = Pipeline(verbose=False)
    p.set_steps([(lambda d: {"a": d.get("value", 0) + 1}, "A", "v1.0")])
    return p


def pipeline_b():
    p = Pipeline(verbose=False)
    p.set_steps([(lambda d: {"b": d.get("a", 0) * 2}, "B", "v1.0")])
    return p


def main():
    main_pipeline = Pipeline(verbose=True)
    main_pipeline.set_steps([
        (pipeline_a().run, "Pipeline A", "v1.0"),
        (pipeline_b().run, "Pipeline B", "v1.0"),
    ])
    
    result = main_pipeline.run({"value": 10})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
