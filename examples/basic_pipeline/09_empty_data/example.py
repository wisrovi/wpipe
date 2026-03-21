"""
Basic Pipeline - Empty Data Handling

Handling missing or empty input data.
"""

from wpipe import Pipeline


def step_a(data):
    value = data.get("value", 0)
    return {"processed": value * 2}


def step_b(data):
    value = data.get("processed", 0)
    multiplier = data.get("multiplier", 1)
    return {"result": value * multiplier}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps([
        (step_a, "Step A", "v1.0"),
        (step_b, "Step B", "v1.0"),
    ])

    result = pipeline.run({})
    print(f"Result with empty data: {result}")
    assert result["result"] == 0

    result2 = pipeline.run({"value": 10, "multiplier": 3})
    print(f"Result with data: {result2}")
    assert result2["result"] == 60


if __name__ == "__main__":
    main()
