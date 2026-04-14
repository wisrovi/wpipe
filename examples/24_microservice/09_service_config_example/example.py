"""
Example 09: Dynamic Configuration

Demonstrates loading configuration dynamically.
"""

from wpipe import Pipeline


def get_config_value(data: dict) -> dict:
    """Loads configuration value.

    Args:
        data: Dictionary containing data.

    Returns:
        Dictionary with configuration loaded status.

    Example:
        >>> result = get_config_value({})
        >>> print(result["config_loaded"])
        True
    """
    return {"config_loaded": True}


class ConfigurableService:
    """Service with dynamic configuration support.

    Attributes:
        config: Configuration dictionary.
        pipeline: Processing pipeline instance.
    """

    def __init__(self, config: dict) -> None:
        """Initializes the configurable service.

        Args:
            config: Dictionary containing service configuration.
        """
        self.config = config
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps([(get_config_value, "Load Config", "v1.0")])

    def handle(self, data: dict) -> dict:
        """Handles request with dynamic configuration.

        Args:
            data: Dictionary containing data to process.

        Returns:
            Dictionary with handling result.

        Example:
            >>> config = {"timeout": 30, "max_retries": 3}
            >>> service = ConfigurableService(config)
            >>> result = service.handle({})
            >>> print(result["config_loaded"])
            True
        """
        return self.pipeline.run(data)


def main() -> None:
    """Runs the configurable service example."""
    config = {"timeout": 30, "max_retries": 3}
    service = ConfigurableService(config)

    service.handle({})
    print(f"Service configured with: {service.config}")


if __name__ == "__main__":
    main()
