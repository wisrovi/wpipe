"""
04 Basic Pipeline - Using get with Defaults

Shows how to safely access data with default values.
"""

from wpipe import Pipeline


def step_with_defaults(data):
    value = data.get("value", 100)
    multiplier = data.get("multiplier", 2)
    return {"result": value * multiplier}


def process_result(data):
    result = data.get("result", 0)
    return {"status": "completed", "value": result * 10}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (step_with_defaults, "Step with Defaults", "v1.0"),
            (process_result, "Process Result", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Result: {result}")
    assert result["result"] == 200
    assert result["value"] == 2000


if __name__ == "__main__":
    main()
