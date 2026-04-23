"""
Progress management for WPipe pipelines.

This module provides a singleton manager for handling Rich-based progress bars
across multiple pipeline executions.
"""

from typing import Any, Optional

from rich.progress import Progress


class ProgressManager:
    """
    Singleton manager for Rich Progress bars.

    Ensures that a single progress instance is shared across the application.
    """

    _instance: Optional["ProgressManager"] = None

    def __new__(cls) -> "ProgressManager":
        """
        Create or return the singleton instance.

        Returns:
            ProgressManager: The shared instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.progress = Progress()
        return cls._instance

    def __init__(self) -> None:
        """Initialize the instance (called after __new__)."""


    def __enter__(self) -> Progress:
        """
        Enter context manager for progress tracking.

        Returns:
            Progress: The Rich progress instance.
        """
        return self.progress.__enter__()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        Exit context manager for progress tracking.

        Args:
            exc_type: Exception type if an error occurred.
            exc_val: Exception value.
            exc_tb: Exception traceback.
        """
        self.progress.__exit__(exc_type, exc_val, exc_tb)
