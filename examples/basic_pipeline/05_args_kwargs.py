"""
05 Basic Pipeline - Using *args and **kwargs

Demonstrates passing additional arguments to pipeline steps.
"""

from wpipe import Pipeline


def transform_data(data, multiplier=1, offset=0):
    value = data.get("value", 0)
    return {"transformed": (value * multiplier) + offset}


def validate_data(data, min_val=0, max_val=100):
    value = data.get("transformed", 0)
    in_range = min_val <= value <= max_val
    return {"valid": in_range, "value": value}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (transform_data, "Transform Data", "v1.0"),
            (validate_data, "Validate Data", "v1.0"),
        ]
    )

    result = pipeline.run({"value": 10}, multiplier=2, offset=5)

    print(f"Result: {result}")
    assert result["transformed"] == 25
    assert result["valid"] is True
    assert result["value"] == 25


if __name__ == "__main__":
    main()
