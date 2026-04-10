"""
Example 05: Health Check Endpoint

Demonstrates implementing a health check for microservice monitoring.
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
        >>> result = process_step({"test": "data"})
        >>> print(result["processed"])
        True
    """
    return {"status": "ok", "processed": True}


class HealthCheckService:
    """Service with health check capability.

    Attributes:
        name: Service name identifier.
        pipeline: Processing pipeline instance.
        logger: Logger instance for the service.
    """

    def __init__(self, name: str = "health_service") -> None:
        """Initializes the health check service.

        Args:
            name: Service name identifier. Defaults to "health_service".
        """
        self.name = name
        self.logger = new_logger(process_name=name)
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps([(process_step, "Process", "v1.0")])

    def health_check(self) -> dict:
        """Performs health check on the service.

        Returns:
            Dictionary with health status information.

        Example:
            >>> service = HealthCheckService("test")
            >>> status = service.health_check()
            >>> print(status["status"])
            healthy
        """
        return {"service": self.name, "status": "healthy", "pipeline_ready": True}

    def process(self, data: dict) -> dict:
        """Processes data through the pipeline.

        Args:
            data: Dictionary containing data to process.

        Returns:
            Dictionary with processing result.

        Example:
            >>> service = HealthCheckService("test")
            >>> result = service.process({"test": "data"})
            >>> print(result["processed"])
            True
        """
        return self.pipeline.run(data)


def main() -> None:
    """Runs the health check service example."""
    service = HealthCheckService("test_service")

    print("Health check:", service.health_check())
    print("Process result:", service.process({"test": "data"}))


if __name__ == "__main__":
    main()
