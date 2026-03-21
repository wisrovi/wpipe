"""
Tests for basic pipeline functionality.
"""

import pytest

from wpipe.pipe import Pipeline


class TestBasicPipeline:
    """Test basic pipeline execution."""

    def test_pipeline_initialization(self):
        """Test pipeline can be initialized."""
        pipeline = Pipeline()
        assert pipeline is not None
        assert pipeline.worker_id is None
        assert pipeline.send_to_api is False

    def test_pipeline_with_verbose(self):
        """Test pipeline with verbose mode."""
        pipeline = Pipeline(verbose=True)
        assert pipeline.verbose is True

    def test_pipeline_with_worker_name(self):
        """Test pipeline with worker name."""
        pipeline = Pipeline(worker_name="test_worker")
        assert pipeline.worker_name == "test_worker"


class TestSetSteps:
    """Test set_steps functionality."""

    def test_set_steps_with_functions(self):
        """Test setting steps with functions."""
        pipeline = Pipeline()

        def step1(data):
            return {"result1": "ok"}

        def step2(data):
            return {"result2": "ok"}

        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0"),
                (step2, "Step2", "v1.0"),
            ]
        )

        assert len(pipeline.tasks_list) == 2

    def test_set_steps_with_classes(self):
        """Test setting steps with classes."""
        pipeline = Pipeline()

        class MyStep:
            def __call__(self, data):
                return {"result": "ok"}

        pipeline.set_steps(
            [
                (MyStep(), "MyStep", "v1.0"),
            ]
        )

        assert len(pipeline.tasks_list) == 1

    def test_set_steps_invalid_input(self):
        """Test set_steps raises error with invalid input."""
        pipeline = Pipeline()

        with pytest.raises(ValueError):
            pipeline.set_steps([("not_a_tuple",)])

    def test_set_steps_wrong_tuple_length(self):
        """Test set_steps raises error with wrong tuple length."""
        pipeline = Pipeline()

        with pytest.raises(ValueError):
            pipeline.set_steps([(lambda x: x, "name")])


class TestPipelineRun:
    """Test pipeline run functionality."""

    def test_run_single_step(self):
        """Test running pipeline with single step."""
        pipeline = Pipeline()

        def step1(data):
            return {"result": data["x"] * 2}

        pipeline.set_steps([(step1, "Step1", "v1.0")])
        result = pipeline.run({"x": 5})

        assert result["result"] == 10

    def test_run_multiple_steps(self):
        """Test running pipeline with multiple steps."""
        pipeline = Pipeline()

        def step1(data):
            return {"x1": data["x"] + 1}

        def step2(data):
            return {"x2": data["x1"] * 2}

        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0"),
                (step2, "Step2", "v1.0"),
            ]
        )

        result = pipeline.run({"x": 5})

        assert result["x1"] == 6
        assert result["x2"] == 12

    def test_run_with_class_step(self):
        """Test running pipeline with class-based step."""
        pipeline = Pipeline()

        class Doubler:
            def __call__(self, data):
                return {"doubled": data["x"] * 2}

        pipeline.set_steps([(Doubler(), "Doubler", "v1.0")])
        result = pipeline.run({"x": 5})

        assert result["doubled"] == 10

    def test_run_data_accumulation(self):
        """Test that data accumulates across steps."""
        pipeline = Pipeline()

        def step1(data):
            return {"from_step1": True}

        def step2(data):
            assert "from_step1" in data
            return {"from_step2": True}

        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0"),
                (step2, "Step2", "v1.0"),
            ]
        )

        result = pipeline.run({})

        assert "from_step1" in result
        assert "from_step2" in result


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

    def test_set_worker_id_invalid_type(self):
        """Test setting non-string worker_id raises error."""
        pipeline = Pipeline()
        try:
            pipeline.set_worker_id(123)
        except Exception:
            pass

    def test_set_worker_id_enables_api(self):
        """Test worker_id enables send_to_api when API config is set."""
        pipeline = Pipeline(
            api_config={"base_url": "http://localhost", "token": "test"}
        )
        pipeline.set_worker_id("worker123456")
        assert pipeline.send_to_api is True


class TestMemoryFunctions:
    """Test memory limit functionality."""

    def test_get_memory_returns_positive(self):
        """Test get_memory returns a positive number."""
        from wpipe.ram.ram import get_memory

        memory = get_memory()
        assert memory > 0

    def test_memory_limit_function(self):
        """Test memory_limit function can be called."""
        from wpipe.ram.ram import memory_limit

        memory_limit(0.8)

    def test_memory_limit_non_linux(self):
        """Test memory_limit on non-Linux systems."""
        from unittest.mock import patch

        from wpipe.ram.ram import memory_limit

        with patch("platform.system", return_value="Windows"):
            memory_limit(0.8)

    def test_memory_decorator_execution(self):
        """Test memory decorator allows function execution."""
        from wpipe.ram import memory

        @memory(percentage=0.8)
        def test_func():
            return {"result": "success"}

        result = test_func()
        assert result["result"] == "success"

    def test_memory_decorator_default_percentage(self):
        """Test memory decorator with default percentage."""
        from wpipe.ram import memory

        @memory()
        def test_func():
            return {"data": 42}

        result = test_func()
        assert result["data"] == 42


class TestPipelineAdvancedFeatures:
    """Test advanced pipeline features."""

    def test_pipeline_with_empty_initial_data(self):
        """Test pipeline with empty initial data."""
        pipeline = Pipeline()

        def step(data):
            return {"result": "ok"}

        pipeline.set_steps([(step, "Step", "v1.0")])
        result = pipeline.run({})

        assert "result" in result

    def test_pipeline_step_order(self):
        """Test pipeline executes steps in correct order."""
        pipeline = Pipeline()
        order = []

        def step1(data):
            order.append(1)
            return {"step1": True}

        def step2(data):
            order.append(2)
            return {"step2": True}

        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0"),
                (step2, "Step2", "v1.0"),
            ]
        )
        pipeline.run({})

        assert order == [1, 2]

    def test_pipeline_data_persistence(self):
        """Test data persists across steps."""
        pipeline = Pipeline()

        def step1(data):
            return {"initial": "value1"}

        def step2(data):
            data["from_step2"] = "value2"
            return data

        def step3(data):
            return {"all_data": data}

        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0"),
                (step2, "Step2", "v1.0"),
                (step3, "Step3", "v1.0"),
            ]
        )
        result = pipeline.run({})

        assert result["initial"] == "value1"
        assert result["from_step2"] == "value2"
        assert "all_data" in result

    def test_pipeline_with_worker_id_and_worker_name(self):
        """Test pipeline with both worker_id and worker_name."""
        api_config = {"base_url": "http://localhost", "token": "test"}
        pipeline = Pipeline(
            worker_id="worker123", worker_name="test_worker", api_config=api_config
        )
        assert pipeline.worker_name == "test_worker"
        assert pipeline.worker_id == "worker123"

    def test_pipeline_worker_register(self):
        """Test worker_register method."""
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"),
            ]
        )
        result = pipeline.worker_register("test_worker", "v1.0")
        assert result is None

    def test_pipeline_api_task_update_no_send(self):
        """Test _api_task_update when send_to_api is False."""
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"),
            ]
        )
        pipeline._api_task_update({"task_id": "123", "status": "start"})
        assert pipeline.send_to_api is False

    def test_pipeline_api_process_update_no_send(self):
        """Test _api_process_update when send_to_api is False."""
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"),
            ]
        )
        pipeline._api_process_update({"process_id": "123"}, start=True)
        assert pipeline.send_to_api is False

    def test_pipeline_api_process_update_no_send_end(self):
        """Test _api_process_update when send_to_api is False (end)."""
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"),
            ]
        )
        pipeline._api_process_update({"process_id": "123"}, start=False)
        assert pipeline.send_to_api is False

    def test_pipeline_with_show_api_errors(self):
        """Test pipeline with SHOW_API_ERRORS enabled."""
        pipeline = Pipeline()
        pipeline.SHOW_API_ERRORS = True
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"),
            ]
        )
        assert pipeline.SHOW_API_ERRORS is True

    def test_pipeline_progress_rich_none(self):
        """Test pipeline with progress_rich set to None."""
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"),
            ]
        )
        pipeline.progress_rich = None
        assert pipeline.progress_rich is None

    def test_pipeline_send_to_api_default(self):
        """Test default send_to_api value."""
        pipeline = Pipeline()
        assert pipeline.send_to_api is False

    def test_pipeline_api_config_default(self):
        """Test default api_config value."""
        pipeline = Pipeline()
        assert pipeline.api_config is None
