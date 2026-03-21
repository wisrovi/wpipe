"""
Basic Pipeline - Class-Based Steps

Pipeline steps using classes with __call__ method.
Classes can maintain state between executions.
"""

from wpipe import Pipeline


class DoubleValue:
    """Double the input value."""

    def __call__(self, data: dict) -> dict:
        """Double the value from input data.

        Args:
            data: Dictionary containing 'value' key.

        Returns:
            Dictionary with 'doubled' key containing doubled value.

        Example:
            >>> DoubleValue()({"value": 10})
            {"doubled": 20}
        """
        return {"doubled": data["value"] * 2}


class AddFive:
    """Add 5 to the doubled value."""

    def __call__(self, data: dict) -> dict:
        """Add 5 to the doubled value from input data.

        Args:
            data: Dictionary containing 'doubled' key.

        Returns:
            Dictionary with 'added' key containing result.

        Example:
            >>> AddFive()({"doubled": 20})
            {"added": 25}
        """
        return {"added": data["doubled"] + 5}


class FormatOutput:
    """Format the final output as a string."""

    def __call__(self, data: dict) -> dict:
        """Format the added value as output string.

        Args:
            data: Dictionary containing 'added' key.

        Returns:
            Dictionary with 'output' key containing formatted string.

        Example:
            >>> FormatOutput()({"added": 25})
            {"output": "Result: 25"}
        """
        return {"output": f"Result: {data['added']}"}


def main() -> None:
    """Run the class-based steps example.

    Demonstrates:
        - Using classes as pipeline steps
        - Maintaining state via __call__ method
        - Chaining class instances as steps
    """
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
