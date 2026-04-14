"""
Example 09: Service Dependencies

Demonstrates managing service dependencies.
"""

from wpipe import Pipeline


def process_step(data: dict) -> dict:
    """Processes data through the pipeline step.

    Args:
        data: Dictionary containing data to process.

    Returns:
        Dictionary with processing status.

    Example:
        >>> result = process_step({})
        >>> print(result["processed"])
        True
    """
    return {"processed": True}


class DependentService:
    """Service that depends on external dependencies.

    Attributes:
        dependency: The dependency that must be ready.
        pipeline: Processing pipeline instance.
    """

    def __init__(self, dependency: "MockDependency") -> None:
        """Initializes the dependent service.

        Args:
            dependency: Object with is_ready() method.
        """
        self.dependency = dependency
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps([(process_step, "Process", "v1.0")])

    def handle(self, data: dict) -> dict:
        """Handles request if dependency is ready.

        Args:
            data: Dictionary containing data to process.

        Returns:
            Dictionary with handling result or error.

        Example:
            >>> dep = MockDependency()
            >>> service = DependentService(dep)
            >>> result = service.handle({})
            >>> print(result["processed"])
            True
        """
        if not self.dependency.is_ready():
            return {"error": "Dependency not ready"}
        return self.pipeline.run(data)


class MockDependency:
    """Mock dependency for testing purposes.

    Attributes:
        ready: Whether the dependency is ready.
    """

    def __init__(self) -> None:
        """Initializes the mock dependency."""
        self.ready = True

    def is_ready(self) -> bool:
        """Checks if the dependency is ready.

        Returns:
            Boolean indicating readiness.
        """
        return self.ready


def main() -> None:
    """Runs the dependent service example."""
    dep = MockDependency()
    service = DependentService(dep)

    result = service.handle({})
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
