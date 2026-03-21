"""
Basic Pipeline - Mixed Functions and Classes

Combining functions and classes in same pipeline.
"""

from wpipe import Pipeline


def extract_numbers(data: dict) -> dict:
    """Extract a list of numbers.

    Args:
        data: Input dictionary (not used).

    Returns:
        Dictionary with 'numbers' key containing list [1, 2, 3, 4, 5].

    Example:
        >>> extract_numbers({})
        {"numbers": [1, 2, 3, 4, 5]}
    """
    return {"numbers": [1, 2, 3, 4, 5]}


class SumNumbers:
    """Sum a list of numbers."""

    def __call__(self, data: dict) -> dict:
        """Sum all numbers from input data.

        Args:
            data: Dictionary containing 'numbers' key with list of numbers.

        Returns:
            Dictionary with 'sum' key containing total.

        Example:
            >>> SumNumbers()({"numbers": [1, 2, 3, 4, 5]})
            {"sum": 15}
        """
        return {"sum": sum(data["numbers"])}


def calculate_average(data: dict) -> dict:
    """Calculate average of numbers.

    Args:
        data: Dictionary containing 'sum' and 'numbers' keys.

    Returns:
        Dictionary with 'average' key containing calculated average.

    Example:
        >>> calculate_average({"sum": 15, "numbers": [1, 2, 3, 4, 5]})
        {"average": 3.0}
    """
    return {"average": data["sum"] / len(data["numbers"])}


def main() -> None:
    """Run the mixed steps example.

    Demonstrates:
        - Combining functions and classes
        - Processing list data
        - Calculating aggregate values
    """
    pipeline = Pipeline(verbose=True)

    pipeline.set_steps(
        [
            (extract_numbers, "Extract Numbers", "v1.0"),
            (SumNumbers(), "Sum Numbers", "v1.0"),
            (calculate_average, "Calculate Average", "v1.0"),
        ]
    )

    result = pipeline.run({})

    print(f"Result: {result}")
    assert result["sum"] == 15
    assert result["average"] == 3.0


if __name__ == "__main__":
    main()
