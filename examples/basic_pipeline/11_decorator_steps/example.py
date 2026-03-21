"""
Basic Pipeline - Decorator Steps

Using decorator pattern with pipeline steps.
"""

from wpipe import Pipeline


def logger(func):
    def wrapper(data):
        print(f"  [LOG] Calling {func.__name__}")
        result = func(data)
        print(f"  [LOG] {func.__name__} returned: {result}")
        return result
    return wrapper


@logger
def step_a(data):
    return {"a": data.get("value", 0) + 1}


@logger
def step_b(data):
    return {"b": data.get("a", 0) * 2}


def main():
    pipeline = Pipeline(verbose=False)
    pipeline.set_steps([
        (step_a, "Step A", "v1.0"),
        (step_b, "Step B", "v1.0"),
    ])
    result = pipeline.run({"value": 5})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
