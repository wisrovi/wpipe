"""
Example 06: Service State Management

Demonstrates managing service state across requests.
"""

from wpipe import Pipeline
from wpipe.log import new_logger


def process_step(data: dict) -> dict:
    """Processes data through the pipeline step.

    Args:
        data: Dictionary containing data to process.

    Returns:
        Dictionary with processing status.

    Example:
        >>> result = process_step({"id": 1})
        >>> print(result["processed"])
        True
    """
    return {"processed": True}


class StatefulService:
    """Service that maintains state across requests.

    Attributes:
        request_count: Number of requests processed.
        logger: Logger instance for the service.
    """

    def __init__(self) -> None:
        """Initializes the stateful service."""
        self.request_count = 0
        self.logger = new_logger("stateful_service")

    def process(self, data: dict) -> dict:
        """Processes data and increments request counter.

        Args:
            data: Dictionary containing data to process.

        Returns:
            Dictionary with processing result.

        Example:
            >>> service = StatefulService()
            >>> result = service.process({"id": 1})
            >>> print(service.request_count)
            1
        """
        self.request_count += 1
        self.logger.info(f"Request #{self.request_count}")

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([(process_step, "Process", "v1.0")])

        return pipeline.run(data)


def main() -> None:
    """Runs the stateful service example."""
    service = StatefulService()

    service.process({"id": 1})
    service.process({"id": 2})

    print(f"Total requests: {service.request_count}")


if __name__ == "__main__":
    main()
