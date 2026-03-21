"""
Basic Pipeline - Multiple Runs

Running same pipeline with different inputs.
"""

from wpipe import Pipeline


def transform(data):
    return {"transformed": data["value"] * 2}


def validate(data):
    return {"valid": data["transformed"] > 0}


def format_output(data):
    return {"output": f"Value is {data['transformed']}, valid: {data['valid']}"}


def run_for_value(value):
    pipeline = Pipeline(verbose=False)
    pipeline.set_steps([
        (transform, "Transform", "v1.0"),
        (validate, "Validate", "v1.0"),
        (format_output, "Format", "v1.0"),
    ])
    return pipeline.run({"value": value})


def main():
    values = [5, 10, 15, 20]
    results = [run_for_value(v) for v in values]

    for i, r in enumerate(results):
        print(f"Input: {values[i]} -> {r['output']}")
        assert r["valid"] is True


if __name__ == "__main__":
    main()
