"""
Exception module for pipeline errors.
"""

from wpipe.log import new_logger

logger = new_logger()


class Codes:
    """Error codes for pipeline exceptions."""

    UPDATE_TASK = 505
    UPDATE_PROCESS_ERROR = 504
    UPDATE_PROCESS_OK = 503
    TASK_FAILED = 502
    API_ERROR = 501


class ApiError(Exception):
    """Exception for API-related errors."""

    def __init__(self, message: str, error_code: int) -> None:
        """
        Initialize ApiError.

        Args:
            message: Error message.
            error_code: Error code from Codes class.
        """
        super().__init__(message)
        self.error_code = error_code
        logger.error(message)


class TaskError(Exception):
    """Exception for task-related errors."""

    def __init__(self, message: str, error_code: int) -> None:
        """
        Initialize TaskError.

        Args:
            message: Error message.
            error_code: Error code from Codes class.
        """
        super().__init__(message)
        self.error_code = error_code

    def __str__(self) -> str:
        """Return string representation."""
        return f"[Error Code: {self.error_code}] {super().__str__()}"


class ProcessError(Exception):
    """Exception for process-related errors."""

    def __init__(self, message: str, error_code: int) -> None:
        """
        Initialize ProcessError.

        Args:
            message: Error message.
            error_code: Error code from Codes class.
        """
        super().__init__(message)
        self.error_code = error_code
