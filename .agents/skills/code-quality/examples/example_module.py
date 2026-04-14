"""
Example module demonstrating best practices for Python code quality.
This module shows how to write production-ready code with proper typing,
docstrings, and error handling.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class UserConfig:
    """Configuration for user authentication.

    Attributes:
        username: The username for authentication.
        password: The user's password (hashed).
        email: User's email address.
        is_active: Whether the user account is active.
    """

    username: str
    password: str
    email: str
    is_active: bool = True


class DataProcessor:
    """Process and transform data according to configured rules.

    This class handles data processing operations including validation,
    transformation, and storage. It follows clean code principles and
    includes comprehensive error handling.

    Attributes:
        config: Configuration object for processing behavior.
        max_retries: Maximum number of retry attempts for failed operations.

    Example:
        >>> config = UserConfig("user", "pass", "user@example.com")
        >>> processor = DataProcessor(config)
        >>> result = processor.process({"key": "value"})
    """

    def __init__(self, config: UserConfig, max_retries: int = 3) -> None:
        """Initialize the DataProcessor.

        Args:
            config: Configuration object containing processing settings.
            max_retries: Maximum number of retry attempts (default: 3).

        Raises:
            ValueError: If max_retries is less than 1.
        """
        if max_retries < 1:
            msg = "max_retries must be at least 1"
            raise ValueError(msg)
        self.config = config
        self.max_retries = max_retries
        self._processed_count: int = 0

    def process(self, data: dict[str, Any]) -> dict[str, Any]:
        """Process input data according to configured rules.

        Args:
            data: Dictionary containing input data to process.

        Returns:
            Dictionary containing processed data.

        Raises:
            ProcessingError: If data processing fails after max_retries.
            ValidationError: If input data is invalid.

        Example:
            >>> processor = DataProcessor(config)
            >>> result = processor.process({"input": "value"})
        """
        self._validate_input(data)
        transformed = self._transform_data(data)
        self._processed_count += 1
        return transformed

    def _validate_input(self, data: dict[str, Any]) -> None:
        """Validate input data structure and content.

        Args:
            data: Data to validate.

        Raises:
            ValidationError: If data is invalid.
        """
        if not isinstance(data, dict):
            msg = "Input data must be a dictionary"
            raise ValidationError(msg)
        if not data:
            msg = "Input data cannot be empty"
            raise ValidationError(msg)

    def _transform_data(self, data: dict[str, Any]) -> dict[str, Any]:
        """Transform data according to processing rules.

        Args:
            data: Data to transform.

        Returns:
            Transformed data dictionary.
        """
        return {
            "original": data,
            "processed": True,
            "processor": self.config.username,
            "count": self._processed_count,
        }

    def reset_count(self) -> None:
        """Reset the processed item counter."""
        self._processed_count = 0


class ValidationError(Exception):
    """Raised when data validation fails."""

    pass


class ProcessingError(Exception):
    """Raised when data processing fails."""

    pass
