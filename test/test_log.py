"""
Tests for logging functionality.
"""

import os
import pytest
from wpipe.log import new_logger


class TestLogger:
    """Test logger creation and configuration."""

    def test_new_logger_creation(self, temp_dir):
        """Test creating a new logger."""
        log_dir = os.path.join(temp_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        logger = new_logger(process_name="test_process", path_file=log_dir)
        assert logger is not None

    def test_new_logger_default_parameters(self):
        """Test logger with default parameters."""
        logger = new_logger()
        assert logger is not None

    def test_new_logger_custom_process_name(self):
        """Test logger with custom process name."""
        logger = new_logger(process_name="custom_process")
        assert logger is not None

    def test_new_logger_returns_logger_object(self):
        """Test that new_logger returns a logger object."""
        logger = new_logger()
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "debug")
