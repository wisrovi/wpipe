"""
Tests for exceptions module.
"""

import pytest
from wpipe.exception import ApiError, TaskError, ProcessError, Codes


class TestCodes:
    """Test error codes."""

    def test_error_codes_exist(self):
        """Test all error codes are defined."""
        assert Codes.UPDATE_TASK == 505
        assert Codes.UPDATE_PROCESS_ERROR == 504
        assert Codes.UPDATE_PROCESS_OK == 503
        assert Codes.TASK_FAILED == 502
        assert Codes.API_ERROR == 501


class TestApiError:
    """Test ApiError exception."""

    def test_api_error_initialization(self):
        """Test ApiError can be initialized."""
        error = ApiError("Test error", Codes.API_ERROR)
        assert error.error_code == Codes.API_ERROR
        assert str(error) == "Test error"

    def test_api_error_inherits_exception(self):
        """Test ApiError inherits from Exception."""
        error = ApiError("Test", Codes.API_ERROR)
        assert isinstance(error, Exception)


class TestTaskError:
    """Test TaskError exception."""

    def test_task_error_initialization(self):
        """Test TaskError can be initialized."""
        error = TaskError("Task failed", Codes.TASK_FAILED)
        assert error.error_code == Codes.TASK_FAILED

    def test_task_error_string_representation(self):
        """Test TaskError string representation."""
        error = TaskError("Task failed", Codes.TASK_FAILED)
        error_str = str(error)
        assert "502" in error_str or "Task failed" in error_str

    def test_task_error_inherits_exception(self):
        """Test TaskError inherits from Exception."""
        error = TaskError("Test", Codes.TASK_FAILED)
        assert isinstance(error, Exception)


class TestProcessError:
    """Test ProcessError exception."""

    def test_process_error_initialization(self):
        """Test ProcessError can be initialized."""
        error = ProcessError("Process failed", Codes.TASK_FAILED)
        assert error.error_code == Codes.TASK_FAILED

    def test_process_error_inherits_exception(self):
        """Test ProcessError inherits from Exception."""
        error = ProcessError("Test", Codes.TASK_FAILED)
        assert isinstance(error, Exception)
