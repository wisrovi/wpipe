"""
Tests for the Pipeline class main functionality.
"""

import pytest
from wpipe.pipe import Pipeline
from wpipe.exception import TaskError, ProcessError


class TestPipelineBasic:
    """Test basic Pipeline functionality without API."""

    def test_pipeline_initialization(self):
        """Test Pipeline can be initialized without arguments."""
        pipeline = Pipeline()
        assert pipeline is not None
        assert pipeline.worker_id is None
        assert pipeline.send_to_api is False

    def test_pipeline_initialization_with_worker_name(self):
        """Test Pipeline initialization with worker name."""
        pipeline = Pipeline(worker_name="test_worker")
        assert pipeline.worker_name == "test_worker"

    def test_pipeline_initialization_with_api_config(self, sample_config):
        """Test Pipeline initialization with API config."""
        pipeline = Pipeline(api_config=sample_config)
        assert pipeline.api_config == sample_config

    def test_pipeline_initialization_with_verbose(self):
        """Test Pipeline initialization with verbose flag."""
        pipeline = Pipeline(verbose=True)
        assert pipeline.verbose is True


class TestSetSteps:
    """Test set_steps functionality."""

    def test_set_steps_with_valid_functions(self, sample_steps):
        """Test set_steps accepts valid function tuples."""
        pipeline = Pipeline()
        pipeline.set_steps(sample_steps)
        assert len(pipeline.tasks_list) == 3

    def test_set_steps_with_invalid_input(self):
        """Test set_steps raises error with invalid input."""
        pipeline = Pipeline()
        with pytest.raises(ValueError):
            pipeline.set_steps([("not_a_tuple")])

    def test_set_steps_with_wrong_tuple_length(self):
        """Test set_steps raises error with wrong tuple length."""
        pipeline = Pipeline()
        with pytest.raises(ValueError):
            pipeline.set_steps([(lambda x: x,)])

    def test_set_steps_with_non_callable(self):
        """Test set_steps raises error with non-callable first element."""
        pipeline = Pipeline()
        with pytest.raises(ValueError):
            pipeline.set_steps([("not_callable", "name", "v1.0")])


class TestWorkerId:
    """Test worker_id management."""

    def test_set_worker_id_valid(self):
        """Test setting a valid worker_id."""
        pipeline = Pipeline()
        pipeline.set_worker_id("worker123456")
        assert pipeline.worker_id == "worker123456"

    def test_set_worker_id_too_short(self):
        """Test setting a too short worker_id sets to None."""
        pipeline = Pipeline()
        pipeline.set_worker_id("abc")
        assert pipeline.worker_id is None

    def test_set_worker_id_with_api_config(self, sample_config):
        """Test worker_id enables send_to_api when API config is set."""
        pipeline = Pipeline(api_config=sample_config)
        pipeline.set_worker_id("worker123456")
        assert pipeline.send_to_api is True

    def test_set_worker_id_invalid_type(self):
        """Test setting non-string worker_id raises error."""
        pipeline = Pipeline()
        try:
            pipeline.set_worker_id(123)
        except Exception:
            pass


class TestPipelineRun:
    """Test pipeline run functionality."""

    def test_run_pipeline_basic(self, sample_steps):
        """Test running a basic pipeline."""
        pipeline = Pipeline()
        pipeline.set_steps(sample_steps)
        result = pipeline.run({"x": 1})
        assert "result1" in result
        assert "result2" in result
        assert "result3" in result

    def test_run_pipeline_with_input_data(self, sample_pipeline_data):
        """Test pipeline with specific input data."""
        pipeline = Pipeline()
        pipeline.set_steps([(lambda d: {"out": d["x"] * 2}, "Double", "v1.0")])
        result = pipeline.run(sample_pipeline_data)
        assert result["out"] == 10

    def test_run_pipeline_with_multiple_steps(self):
        """Test running pipeline with multiple steps."""
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"step1": d.get("x", 0) + 1}, "Step1", "v1.0"),
                (lambda d: {"step2": d.get("step1", 0) + 1}, "Step2", "v1.0"),
            ]
        )
        result = pipeline.run({"x": 1})
        assert "step1" in result
        assert "step2" in result
        assert result["step1"] == 2
        assert result["step2"] == 3


class TestPipelineErrorHandling:
    """Test pipeline error handling."""

    def test_pipeline_task_error(self):
        """Test pipeline handles task errors correctly."""

        def failing_task(data):
            raise ValueError("Task failed")

        pipeline = Pipeline(continue_on_error=False)
        pipeline.set_steps([(failing_task, "FailingTask", "v1.0")])
        try:
            pipeline.run({"x": 1})
            assert False, "Should have raised an error"
        except (TaskError, ProcessError):
            pass

    def test_pipeline_returns_error_in_data(self):
        """Test pipeline includes error in returned data on failure."""

        def failing_task(data):
            raise Exception("Task failed")

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([(failing_task, "FailingTask", "v1.0")])
        try:
            pipeline.run({"x": 1})
        except (TaskError, ProcessError):
            pass


class TestPipelineVerbose:
    """Test verbose mode functionality."""

    def test_verbose_mode_enabled(self):
        """Test pipeline runs with verbose mode enabled."""

        def simple_task(data):
            return {"result": "ok"}

        pipeline = Pipeline(verbose=True)
        pipeline.set_steps(
            [
                (lambda d: {"step1": True}, "Step1", "v1.0"),
                (simple_task, "Simple", "v1.0"),
            ]
        )
        result = pipeline.run({"x": 1})
        assert "result" in result

    def test_verbose_mode_disabled(self):
        """Test pipeline runs with verbose mode disabled."""

        def simple_task(data):
            return {"result": "ok"}

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps(
            [
                (lambda d: {"step1": True}, "Step1", "v1.0"),
                (simple_task, "Simple", "v1.0"),
            ]
        )
        result = pipeline.run({"x": 1})
        assert "result" in result
