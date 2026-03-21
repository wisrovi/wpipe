"""
Example 07: Request Validation

Demonstrates validating incoming requests.
"""

from wpipe import Pipeline


def validate_request(data: dict) -> dict:
    """Validates that required field is present.

    Args:
        data: Dictionary containing request data.

    Returns:
        Dictionary with validation result.

    Raises:
        ValueError: If 'required_field' is missing from data.

    Example:
        >>> result = validate_request({"required_field": "present"})
        >>> print(result["validated"])
        True
    """
    if "required_field" not in data:
        raise ValueError("Missing required_field")
    return {"validated": True}


def process(data: dict) -> dict:
    """Processes validated data.

    Args:
        data: Dictionary containing validated data.

    Returns:
        Dictionary with processing status.

    Example:
        >>> result = process({"validated": True})
        >>> print(result["processed"])
        True
    """
    return {"processed": True}


class ValidatingService:
    """Service that validates requests before processing.

    Attributes:
        pipeline: Processing pipeline with validation steps.
    """

    def __init__(self) -> None:
        """Initializes the validating service."""
        self.pipeline = Pipeline(verbose=False)
        self.pipeline.set_steps(
            [
                (validate_request, "Validate", "v1.0"),
                (process, "Process", "v1.0"),
            ]
        )

    def handle(self, data: dict) -> dict:
        """Handles request through validation and processing.

        Args:
            data: Dictionary containing request data.

        Returns:
            Dictionary with handling result.

        Example:
            >>> service = ValidatingService()
            >>> result = service.handle({"required_field": "present"})
            >>> print(result["processed"])
            True
        """
        return self.pipeline.run(data)


def main() -> None:
    """Runs the validating service example."""
    service = ValidatingService()

    result = service.handle({"required_field": "present"})
    print(f"Valid request result: {result}")


if __name__ == "__main__":
    main()
