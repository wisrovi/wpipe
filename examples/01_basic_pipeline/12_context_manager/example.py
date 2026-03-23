"""
Basic Pipeline - Context Manager Steps

Pipeline steps that use context managers.
"""

from wpipe import Pipeline


class FileProcessor:
    """Process values using context manager pattern."""

    def __init__(self) -> None:
        """Initialize processor."""
        self.data: list = []

    def __enter__(self) -> "FileProcessor":
        """Initialize processor.

        Returns:
            Self reference.
        """
        return self

    def __call__(self, data: dict) -> dict:
        """Process value and track count.

        Args:
            data: Dictionary containing 'value' key.

        Returns:
            Dictionary with 'processed' count.

        Example:
            >>> fp = FileProcessor()
            >>> fp({"value": 100})
            {"processed": 1}
        """
        self.data.append(data.get("value", 0))
        return {"processed": len(self.data), "values": list(self.data)}

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Cleanup on exit."""
        pass


def main() -> None:
    """Run the context manager steps example.

    Demonstrates:
        - Using context managers as pipeline steps
        - Maintaining state across calls
        - Cleanup on exit
    """
    pipeline = Pipeline(verbose=True)

    processor = FileProcessor()

    pipeline.set_steps(
        [
            (processor, "Process Files", "v1.0"),
        ]
    )

    result = pipeline.run({"value": 100})
    print(f"Result: {result}")

    result2 = pipeline.run({"value": 200})
    print(f"Result2: {result2}")


if __name__ == "__main__":
    main()
