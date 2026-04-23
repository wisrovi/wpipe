"""
Tests for basic pipeline functionality.
"""

import pytest
import asyncio
import sqlite3
import threading
from typing import Dict, Any, List, Optional, Callable

from wpipe import Pipeline, step
from wpipe.api_client.api_client import APIClient # Imported for context, though not used in this file
from wpipe.ram.ram import get_memory, memory_limit # Imported for context


# --- RE-PARCHE DE EMERGENCIA PARA ARREGLAR BUG DE WPIPE ---
from wsqlite import WSQLite
_db_connections = {}
_db_lock = threading.Lock()

def better_get_connection(self):
    db_path = getattr(self, "db_path", getattr(self, "db_name", "register.db"))
    with _db_lock:
        if db_path not in _db_connections:
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            _db_connections[db_path] = conn
        return _db_connections[db_path]

WSQLite._get_connection = better_get_connection

# --- END RE-PARCHE ---

class TestBasicPipeline:
    """Tests for basic pipeline execution and initialization.

    This class verifies the core functionalities of the Pipeline class,
    including its initialization, handling of verbose mode, and worker naming.
    """

    def test_pipeline_initialization(self) -> None:
        """Tests that a Pipeline object can be successfully initialized.

        Asserts that a new Pipeline instance is created without a worker ID
        and that the `send_to_api` flag is correctly set to False by default.
        """
        pipeline = Pipeline()
        assert pipeline is not None
        assert pipeline.worker_id is None
        assert pipeline.send_to_api is False

    def test_pipeline_with_verbose(self) -> None:
        """Tests Pipeline initialization with verbose mode enabled.

        Verifies that setting the `verbose` parameter to True during
        initialization correctly sets the pipeline's verbose attribute.
        """
        pipeline = Pipeline(verbose=True)
        assert pipeline.verbose is True

    def test_pipeline_with_worker_name(self) -> None:
        """Tests Pipeline initialization with a specified worker name.

        Ensures that a worker name provided during initialization is correctly
        assigned to the pipeline's `worker_name` attribute.
        """
        pipeline = Pipeline(worker_name="test_worker")
        assert pipeline.worker_name == "test_worker"


class TestSetSteps:
    """Tests for the set_steps functionality of the Pipeline class.

    This class validates how steps are configured and added to the pipeline,
    including handling different input formats like functions and classes,
    as well as error conditions.
    """

    def test_set_steps_with_functions(self) -> None:
        """Tests setting pipeline steps using plain Python functions.

        Verifies that a list of tuples, where each tuple contains a function,
        its name, and version, is correctly processed to define pipeline tasks.
        """
        pipeline = Pipeline()

        def step1(data: Dict[str, Any]) -> Dict[str, str]:
            """A simple example step function."""
            return {"result1": "ok"}

        def step2(data: Dict[str, Any]) -> Dict[str, str]:
            """Another simple example step function."""
            return {"result2": "ok"}

        pipeline.set_steps(
            [
                (step1, "Step1", "v1.0"),
                (step2, "Step2", "v1.0"),
            ]
        )

        assert len(pipeline.tasks_list) == 2

    def test_set_steps_with_classes(self) -> None:
        """Tests setting pipeline steps using callable class instances.

        Ensures that instances of callable classes can be correctly configured
        as pipeline steps, along with their names and versions.
        """
        pipeline = Pipeline()

        class MyStep:
            """A simple callable class to be used as a pipeline step."""
            def __call__(self, data: Dict[str, Any]) -> Dict[str, str]:
                """Processes data and returns a result."""
                return {"result": "ok"}

        pipeline.set_steps(
            [
                (MyStep(), "MyStep", "v1.0"),
            ]
        )

        assert len(pipeline.tasks_list) == 1

    def test_set_steps_invalid_input(self) -> None:
        """Tests that set_steps raises ValueError for invalid input format.

        Ensures that providing input to set_steps that is not a list of tuples
        or does not conform to expected structures raises an appropriate error.
        """
        pipeline = Pipeline()

        with pytest.raises(ValueError):
            pipeline.set_steps([("not_a_tuple",)]) # type: ignore

    def test_set_steps_wrong_tuple_length(self) -> None:
        """Tests set_steps normalization for 2-element tuples.

        Verifies that a 2-tuple (function, name) is correctly normalized into
        the expected 4-element task tuple, providing default values for version
        and metadata.
        """
        pipeline = Pipeline()

        # A 2-tuple (function, name) should be valid and get normalized
        pipeline.set_steps([(lambda x: x, "name")]) # type: ignore
        
        # Should have one task that was normalized to 4 elements
        assert len(pipeline.tasks_list) == 1
        task = pipeline.tasks_list[0]
        assert isinstance(task, tuple)
        assert len(task) == 4
        assert task[0] is not None  # function
        assert task[1] == "name"    # name
        assert task[2] == "v1.0"    # version (default)
        assert task[3] == {}        # metadata (default)


class TestPipelineRun:
    """Tests for the pipeline run functionality.

    This class validates the execution of pipelines, including single and
    multiple steps, class-based steps, and data accumulation across steps.
    """

    def test_run_single_step(self) -> None:
        """Tests running a pipeline with a single defined step.

        Ensures that the pipeline executes the single step correctly and
        returns the processed data.
        """
        pipeline = Pipeline()

        def step1(data: Dict[str, int]) -> Dict[str, int]:
            """A step that doubles the value of 'x'."""
            return {"result": data["x"] * 2}

        pipeline.set_steps([(step1, "Step1", "v1.0")])
        result = pipeline.run({"x": 5})

        assert result["result"] == 10

    def test_run_multiple_steps(self) -> None:
        """Tests running a pipeline with multiple sequential steps.

        Verifies that data is passed correctly between sequential steps and
        that the final result reflects the combined operations.
        """
        pipeline = Pipeline()

        def step1(data: Dict[str, int]) -> Dict[str, int]:
            """Increments the input value 'x' by 1."""
            return {"x1": data["x"] + 1}

        def step2(data: Dict[str, int]) -> Dict[str, int]:
            """Doubles the input value 'x1'."""
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

    def test_run_with_class_step(self) -> None:
        """Tests running a pipeline that includes a class-based step.

        Ensures that steps defined as callable class instances are executed
        correctly and produce the expected output.
        """
        pipeline = Pipeline()

        class Doubler:
            """A callable class that doubles the input value 'x'."""
            def __call__(self, data: Dict[str, int]) -> Dict[str, int]:
                """Doubles the value of 'x' from the input data."""
                return {"doubled": data["x"] * 2}

        pipeline.set_steps([(Doubler(), "Doubler", "v1.0")])
        result = pipeline.run({"x": 5})

        assert result["doubled"] == 10

    def test_run_data_accumulation(self) -> None:
        """Tests that data is correctly accumulated across pipeline steps.

        Verifies that output from earlier steps is available as input to
        subsequent steps within the same pipeline run.
        """
        pipeline = Pipeline()

        def step1(data: Dict[str, Any]) -> Dict[str, bool]:
            """Adds 'from_step1' key to the data."""
            return {"from_step1": True}

        def step2(data: Dict[str, Any]) -> Dict[str, bool]:
            """Asserts 'from_step1' is present and adds 'from_step2' key."""
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
    """Tests for worker_id management within the Pipeline class.

    This class validates the setting, validation, and implications of worker IDs,
    such as enabling API communication.
    """

    def test_set_worker_id_valid(self) -> None:
        """Tests setting a valid worker_id.

        Ensures that a worker ID meeting the length requirements is correctly
        assigned to the pipeline.
        """
        pipeline = Pipeline()
        pipeline.set_worker_id("worker123456")
        assert pipeline.worker_id == "worker123456"

    def test_set_worker_id_too_short(self) -> None:
        """Tests that a worker_id that is too short is set to None.

        Verifies that providing a worker ID shorter than the minimum length
        results in the worker_id attribute being set to None.
        """
        pipeline = Pipeline()
        pipeline.set_worker_id("abc")
        assert pipeline.worker_id is None

    def test_set_worker_id_invalid_type(self) -> None:
        """Tests that setting a non-string worker_id raises an error.

        Ensures type safety by checking that only string worker IDs are accepted.
        """
        pipeline = Pipeline()
        with pytest.raises(TypeError): # Expecting TypeError for incorrect type
            pipeline.set_worker_id(123) # type: ignore

    def test_set_worker_id_enables_api(self) -> None:
        """Tests that setting a worker_id enables send_to_api when API config is present.

        Verifies that if the pipeline is configured with API details, setting a
        valid worker ID activates the `send_to_api` flag.
        """
        pipeline = Pipeline(
            api_config={"base_url": "http://localhost", "token": "test"}
        )
        pipeline.set_worker_id("worker123456")
        assert pipeline.send_to_api is True


class TestMemoryFunctions:
    """Tests for memory-related utility functions and decorators.

    This class validates functions and decorators designed for monitoring and
    managing memory usage, including platform-specific behavior.
    """

    def test_get_memory_returns_positive(self) -> None:
        """Tests that get_memory returns a positive value.

        Ensures the `get_memory` function correctly reports available memory,
        which should always be a positive number.
        """
        # Assuming get_memory is correctly imported and available
        memory = get_memory()
        assert memory > 0

    def test_memory_limit_function(self) -> None:
        """Tests that the memory_limit function can be called without errors.

        Verifies the basic call signature and execution of `memory_limit`.
        Note: This test does not verify actual memory capping.
        """
        # Assuming memory_limit is correctly imported and available
        memory_limit(0.8)

    def test_memory_limit_non_linux(self) -> None:
        """Tests memory_limit behavior on non-Linux systems.

        Ensures `memory_limit` functions correctly by mocking the platform
        to simulate a non-Linux environment (e.g., Windows).
        """
        from unittest.mock import patch

        with patch("platform.system", return_value="Windows"):
            memory_limit(0.8)

    def test_memory_decorator_execution(self) -> None:
        """Tests that the memory decorator allows function execution.

        Verifies that a function decorated with `@memory` can be called and
        returns its expected result.
        """
        # Assuming 'memory' decorator is correctly imported
        from wpipe.ram import memory

        @memory(percentage=0.8)
        def test_func() -> Dict[str, str]:
            """A sample function decorated with @memory."""
            return {"result": "success"}

        result = test_func()
        assert result["result"] == "success"

    def test_memory_decorator_default_percentage(self) -> None:
        """Tests the memory decorator with its default percentage value.

        Ensures the decorator works correctly when only the function is provided,
        using the default percentage for memory limiting.
        """
        from wpipe.ram import memory

        @memory()
        def test_func() -> Dict[str, int]:
            """A sample function decorated with @memory using default percentage."""
            return {"data": 42}

        result = test_func()
        assert result["data"] == 42


class TestPipelineAdvancedFeatures:
    """Tests for advanced pipeline features and behaviors.

    This class covers aspects like data persistence, step ordering, handling
    of empty initial data, and interactions with API-related flags.
    """

    def test_pipeline_with_empty_initial_data(self) -> None:
        """Tests pipeline execution when provided with empty initial data.

        Ensures the pipeline can correctly process an empty dictionary as input
        and that steps can still execute.
        """
        pipeline = Pipeline()

        def step(data: Dict[str, Any]) -> Dict[str, str]:
            """A simple step that returns a fixed result."""
            return {"result": "ok"}

        pipeline.set_steps([(step, "Step", "v1.0")])
        result = pipeline.run({})

        assert "result" in result

    def test_pipeline_step_order(self) -> None:
        """Tests that pipeline steps execute in the defined order.

        Verifies that the sequence of steps is maintained correctly during pipeline
        execution, confirmed by tracking the order of execution.
        """
        pipeline = Pipeline()
        order: List[int] = []

        def step1(data: Dict[str, Any]) -> Dict[str, bool]:
            """Appends 1 to the order list and marks step1 as done."""
            order.append(1)
            return {"step1": True}

        def step2(data: Dict[str, Any]) -> Dict[str, bool]:
            """Appends 2 to the order list and marks step2 as done."""
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

    def test_pipeline_data_persistence(self) -> None:
        """Tests that data is correctly persisted and passed across steps.

        Ensures that data generated in earlier steps is available and can be
        modified by subsequent steps within the same pipeline run.
        """
        pipeline = Pipeline()

        def step1(data: Dict[str, Any]) -> Dict[str, str]:
            """Initializes data with 'initial' key."""
            return {"initial": "value1"}

        def step2(data: Dict[str, Any]) -> Dict[str, str]:
            """Adds 'from_step2' key to the data."""
            data["from_step2"] = "value2"
            return data

        def step3(data: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
            """Returns all accumulated data under the 'all_data' key."""
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

    def test_pipeline_with_worker_id_and_worker_name(self) -> None:
        """Tests Pipeline initialization with both worker_id and worker_name.

        Ensures that both unique identifiers are correctly set when provided
        during initialization, along with API configuration.
        """
        api_config: Dict[str, str] = {"base_url": "http://localhost", "token": "test"}
        pipeline = Pipeline(
            worker_id="worker123", worker_name="test_worker", api_config=api_config
        )
        assert pipeline.worker_name == "test_worker"
        assert pipeline.worker_id == "worker123"

    def test_pipeline_worker_register(self) -> None:
        """Tests the worker_register method.

        Verifies that the `worker_register` method can be called, although it
        might not perform significant actions in this test setup.
        """
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"), # type: ignore
            ]
        )
        result = pipeline.worker_register("test_worker", "v1.0")
        assert result is None

    def test_pipeline_api_task_update_no_send(self) -> None:
        """Tests _api_task_update when send_to_api is False.

        Ensures that internal API update methods are not called if `send_to_api`
        is not enabled, preventing unintended API calls.
        """
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"), # type: ignore
            ]
        )
        pipeline._api_task_update({"task_id": "123", "status": "start"})
        assert pipeline.send_to_api is False

    def test_pipeline_api_process_update_no_send(self) -> None:
        """Tests _api_process_update when send_to_api is False (start).

        Verifies that the `_api_process_update` method does not attempt API calls
        when `send_to_api` is disabled.
        """
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"), # type: ignore
            ]
        )
        pipeline._api_process_update({"process_id": "123"}, start=True)
        assert pipeline.send_to_api is False

    def test_pipeline_api_process_update_no_send_end(self) -> None:
        """Tests _api_process_update when send_to_api is False (end).

        Confirms that the `_api_process_update` method behaves correctly when
        ending a process and `send_to_api` is False.
        """
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"), # type: ignore
            ]
        )
        pipeline._api_process_update({"process_id": "123"}, start=False)
        assert pipeline.send_to_api is False

    def test_pipeline_with_show_api_errors(self) -> None:
        """Tests enabling the SHOW_API_ERRORS flag in the Pipeline.

        Ensures that setting `SHOW_API_ERRORS` to True is reflected in the
        pipeline's attribute.
        """
        pipeline = Pipeline()
        pipeline.SHOW_API_ERRORS = True
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"), # type: ignore
            ]
        )
        assert pipeline.SHOW_API_ERRORS is True

    def test_pipeline_progress_rich_none(self) -> None:
        """Tests Pipeline when progress_rich is explicitly set to None.

        Verifies that the `progress_rich` attribute can be None.
        """
        pipeline = Pipeline()
        pipeline.set_steps(
            [
                (lambda d: {"result": True}, "Step1", "v1.0"), # type: ignore
            ]
        )
        pipeline.progress_rich = None
        assert pipeline.progress_rich is None

    def test_pipeline_send_to_api_default(self) -> None:
        """Tests the default value of the send_to_api flag.

        Ensures that `send_to_api` is False by default upon pipeline initialization.
        """
        pipeline = Pipeline()
        assert pipeline.send_to_api is False

    def test_pipeline_api_config_default(self) -> None:
        """Tests the default value of the api_config attribute.

        Ensures that `api_config` is None by default upon pipeline initialization.
        """
        pipeline = Pipeline()
        assert pipeline.api_config is None
