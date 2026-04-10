"""
Example 08: Metrics Collection

Demonstrates collecting service metrics.
"""

import time

from wpipe import Pipeline


def process_step(data: dict) -> dict:
    """Processes data through the pipeline step.

    Args:
        data: Dictionary containing data to process.

    Returns:
        Dictionary with processing status.

    Example:
        >>> result = process_step({"test": "data"})
        >>> print(result["processed"])
        True
    """
    return {"processed": True}


class MetricsService:
    """Service that collects performance metrics.

    Attributes:
        total_requests: Total number of requests processed.
        total_time: Total processing time in seconds.
    """

    def __init__(self) -> None:
        """Initializes the metrics service."""
        self.total_requests = 0
        self.total_time = 0.0

    def handle(self, data: dict) -> dict:
        """Handles request and records metrics.

        Args:
            data: Dictionary containing data to process.

        Returns:
            Dictionary with processing result.

        Example:
            >>> service = MetricsService()
            >>> result = service.handle({})
            >>> print(service.total_requests)
            1
        """
        start = time.time()

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([(process_step, "Process", "v1.0")])
        result = pipeline.run(data)

        elapsed = time.time() - start
        self.total_requests += 1
        self.total_time += elapsed

        return result

    def get_metrics(self) -> dict:
        """Returns collected metrics.

        Returns:
            Dictionary with service metrics.

        Example:
            >>> service = MetricsService()
            >>> service.handle({})
            >>> metrics = service.get_metrics()
            >>> print(metrics["requests"])
            1
        """
        return {
            "requests": self.total_requests,
            "avg_time": self.total_time / max(self.total_requests, 1),
        }


def main() -> None:
    """Runs the metrics service example."""
    service = MetricsService()

    for _ in range(3):
        service.handle({})

    print(f"Metrics: {service.get_metrics()}")


if __name__ == "__main__":
    main()
