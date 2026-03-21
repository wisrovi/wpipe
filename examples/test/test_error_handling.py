"""
Tests for error handling functionality.
"""

from wpipe.exception import ApiError, Codes, ProcessError, TaskError
from wpipe.pipe import Pipeline


class TestExceptionClasses:
    """Test exception classes."""

    def test_error_codes(self):
        """Test error codes are defined."""
        assert Codes.UPDATE_TASK == 505
        assert Codes.UPDATE_PROCESS_ERROR == 504
        assert Codes.UPDATE_PROCESS_OK == 503
        assert Codes.TASK_FAILED == 502
        assert Codes.API_ERROR == 501

    def test_api_error(self):
        """Test ApiError exception."""
        error = ApiError("Test error", Codes.API_ERROR)
        assert error.error_code == Codes.API_ERROR

    def test_task_error(self):
        """Test TaskError exception."""
        error = TaskError("Task failed", Codes.TASK_FAILED)
        assert error.error_code == Codes.TASK_FAILED

    def test_process_error(self):
        """Test ProcessError exception."""
        error = ProcessError("Process failed", Codes.TASK_FAILED)
        assert error.error_code == Codes.TASK_FAILED


class TestPipelineErrors:
    """Test pipeline error handling."""

    def test_task_error_is_raised(self):
        """Test that task errors are raised correctly."""

        def failing_task(data):
            raise ValueError("Task failed")

        pipeline = Pipeline()
        pipeline.set_steps([(failing_task, "FailingTask", "v1.0")])

        try:
            pipeline.run({"x": 1})
            raise AssertionError("Should have raised an error")
        except (TaskError, ProcessError):
            pass

    def test_validation_error(self):
        """Test validation errors in steps."""

        def validate(data):
            if "x" not in data:
                raise ValueError("Missing required field 'x'")
            return {"validated": True}

        pipeline = Pipeline()
        pipeline.set_steps([(validate, "Validate", "v1.0")])

        try:
            pipeline.run({})
        except (TaskError, ProcessError):
            pass

    def test_error_with_custom_exception(self):
        """Test custom exception handling."""

        def failing_task(data):
            raise RuntimeError("Custom error")

        pipeline = Pipeline()
        pipeline.set_steps([(failing_task, "FailingTask", "v1.0")])

        try:
            pipeline.run({"x": 1})
        except (TaskError, ProcessError):
            pass

    def test_error_message_preserved(self):
        """Test that error messages are preserved."""
        error_message = "Specific error message"

        def failing_task(data):
            raise ValueError(error_message)

        pipeline = Pipeline()
        pipeline.set_steps([(failing_task, "FailingTask", "v1.0")])

        try:
            pipeline.run({"x": 1})
        except (TaskError, ProcessError) as e:
            assert error_message in str(e)
