"""
08 Basic Pipeline - Using verbose Mode

Demonstrates the verbose mode for debugging.
"""

from wpipe import Pipeline


def step_a(data):
    return {"a": data["input"] + 1}


def step_b(data):
    return {"b": data["a"] * 2}


def step_c(data):
    return {"c": data["b"] - 1}


def main():
    print("=== Verbose = False ===")
    pipeline = Pipeline(verbose=False)
    pipeline.set_steps(
        [
            (step_a, "Step A", "v1.0"),
            (step_b, "Step B", "v1.0"),
            (step_c, "Step C", "v1.0"),
        ]
    )
    result = pipeline.run({"input": 5})
    print(f"Result: {result}")

    print("\n=== Verbose = True ===")
    pipeline2 = Pipeline(verbose=True)
    pipeline2.set_steps(
        [
            (step_a, "Step A", "v1.0"),
            (step_b, "Step B", "v1.0"),
            (step_c, "Step C", "v1.0"),
        ]
    )
    result2 = pipeline2.run({"input": 5})
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()
