"""
Basic Pipeline - Async Steps

Pipeline steps with async-like processing (simulated).
"""

from wpipe import Pipeline


def step_a(data):
    return {"step": "A", "value": data.get("value", 0)}


def step_b(data):
    return {"step": "B", "value": data.get("value", 0) * 2}


def step_c(data):
    return {"step": "C", "value": data.get("value", 0) + 10}


def main():
    pipeline = Pipeline(verbose=True)
    pipeline.set_steps([
        (step_a, "Step A", "v1.0"),
        (step_b, "Step B", "v1.0"),
        (step_c, "Step C", "v1.0"),
    ])
    
    result = pipeline.run({"value": 5})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
