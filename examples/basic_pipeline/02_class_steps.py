"""
02 Basic Pipeline - Class-Based Steps

Demonstrates using classes as pipeline steps.
Classes must implement __call__ to be used as steps.
"""

from wpipe import Pipeline


class DoubleValue:
    def __call__(self, data):
        return {"doubled": data["value"] * 2}


class AddFive:
    def __call__(self, data):
        return {"added": data["doubled"] + 5}


class FormatOutput:
    def __call__(self, data):
        return {"output": f"Result: {data['added']}"}


def main():
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (DoubleValue(), "Double Value", "v1.0"),
            (AddFive(), "Add Five", "v1.0"),
            (FormatOutput(), "Format Output", "v1.0"),
        ]
    )

    result = pipeline.run({"value": 10})

    print(f"Result: {result}")
    assert result["output"] == "Result: 25"


if __name__ == "__main__":
    main()
