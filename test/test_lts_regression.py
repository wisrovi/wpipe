"""
Regression tests for wpipe LTS backward compatibility.

These tests ensure that the public API remains stable across versions
and that no breaking changes are introduced in the 2.0.x LTS series.
"""

import pytest
import wpipe
from wpipe import (
    Pipeline,
    Condition,
    For,
    APIClient,
    Wsqlite,
    CheckpointManager,
    PipelineExporter,
    ResourceMonitor,
    ResourceMonitorRegistry,
    TypeValidator,
    PipelineContext,
    GenericPipeline,
    TaskTimer,
    TimeoutError,
    timeout_sync,
    timeout_async,
    ParallelExecutor,
    ExecutionMode,
    DAGScheduler,
    PipelineAsStep,
    CompositionHelper,
    NestedPipelineStep,
    step,
    StepRegistry,
    AutoRegister,
    get_step_registry,
    PipelineTracker,
    Metric,
    Severity,
    memory,
    new_logger,
    to_obj,
    auto_dict_input,
    state,
    object_to_dict,
)
from wpipe.pipe.pipe_async import PipelineAsync
from wpipe.decorators import StepRegistry as StepRegistryFromDecorators
from wpipe.tracking import Severity as SeverityFromTracking


# ============================================================
# Version Consistency Tests
# ============================================================

class TestVersionConsistency:
    """Ensure version declarations are consistent."""

    def test_version_attribute_exists(self):
        """wpipe.__version__ should exist."""
        assert hasattr(wpipe, "__version__")
        assert wpipe.__version__

    def test_version_is_string(self):
        """Version should be a string."""
        assert isinstance(wpipe.__version__, str)

    def test_version_starts_with_2(self):
        """LTS version should start with 2."""
        assert wpipe.__version__.startswith("2.")


# ============================================================
# Core API Export Tests
# ============================================================

class TestCoreAPIExports:
    """Ensure all public API elements are importable."""

    def test_pipeline_is_class(self):
        """Pipeline should be a class."""
        assert isinstance(Pipeline, type)

    def test_condition_is_class(self):
        """Condition should be a class."""
        assert isinstance(Condition, type)

    def test_for_is_class(self):
        """For should be a class."""
        assert isinstance(For, type)

    def test_api_client_is_class(self):
        """APIClient should be a class."""
        assert isinstance(APIClient, type)

    def test_wsqlite_is_class(self):
        """Wsqlite should be a class."""
        assert isinstance(Wsqlite, type)

    def test_checkpoint_manager_is_class(self):
        """CheckpointManager should be a class."""
        assert isinstance(CheckpointManager, type)

    def test_exporter_is_class(self):
        """PipelineExporter should be a class."""
        assert isinstance(PipelineExporter, type)

    def test_resource_monitor_is_class(self):
        """ResourceMonitor should be a class."""
        assert isinstance(ResourceMonitor, type)

    def test_resource_monitor_registry_is_class(self):
        """ResourceMonitorRegistry should be a class."""
        assert isinstance(ResourceMonitorRegistry, type)

    def test_type_validator_is_class(self):
        """TypeValidator should be a class."""
        assert isinstance(TypeValidator, type)

    def test_pipeline_context_is_class(self):
        """PipelineContext should be a class."""
        assert isinstance(PipelineContext, type)

    def test_generic_pipeline_is_class(self):
        """GenericPipeline should be a class."""
        assert isinstance(GenericPipeline, type)

    def test_task_timer_is_class(self):
        """TaskTimer should be a class."""
        assert isinstance(TaskTimer, type)

    def test_timeout_error_is_exception(self):
        """TimeoutError should be an exception."""
        assert issubclass(TimeoutError, BaseException)

    def test_parallel_executor_is_class(self):
        """ParallelExecutor should be a class."""
        assert isinstance(ParallelExecutor, type)

    def test_execution_mode_is_enum(self):
        """ExecutionMode should be an enum."""
        assert isinstance(ExecutionMode, type)

    def test_dag_scheduler_is_class(self):
        """DAGScheduler should be a class."""
        assert isinstance(DAGScheduler, type)

    def test_pipeline_as_step_is_class(self):
        """PipelineAsStep should be a class."""
        assert isinstance(PipelineAsStep, type)

    def test_composition_helper_is_class(self):
        """CompositionHelper should be a class."""
        assert isinstance(CompositionHelper, type)

    def test_nested_pipeline_step_is_class(self):
        """NestedPipelineStep should be a class."""
        assert isinstance(NestedPipelineStep, type)

    def test_step_is_callable(self):
        """step decorator should be callable."""
        assert callable(step)

    def test_step_registry_is_class(self):
        """StepRegistry should be a class."""
        assert isinstance(StepRegistry, type)

    def test_auto_register_is_class(self):
        """AutoRegister should be a class."""
        assert isinstance(AutoRegister, type)

    def test_get_step_registry_is_callable(self):
        """get_step_registry should be callable."""
        assert callable(get_step_registry)

    def test_pipeline_tracker_is_class(self):
        """PipelineTracker should be a class."""
        assert isinstance(PipelineTracker, type)

    def test_metric_is_class(self):
        """Metric should be a class."""
        assert isinstance(Metric, type)

    def test_severity_is_enum(self):
        """Severity should be an enum."""
        assert isinstance(Severity, type)

    def test_memory_is_callable(self):
        """memory decorator should be callable."""
        assert callable(memory)

    def test_new_logger_is_callable(self):
        """new_logger should be callable."""
        assert callable(new_logger)


# ============================================================
# Pipeline API Stability Tests
# ============================================================

class TestPipelineAPIStability:
    """Ensure Pipeline API remains stable."""

    def test_pipeline_can_instantiate(self):
        """Pipeline should instantiate without error."""
        p = Pipeline(verbose=False)
        assert p is not None

    def test_pipeline_has_run_method(self):
        """Pipeline should have run method."""
        p = Pipeline(verbose=False)
        assert hasattr(p, "run")
        assert callable(p.run)

    def test_pipeline_has_set_steps_method(self):
        """Pipeline should have set_steps method (Phase 1 API)."""
        p = Pipeline(verbose=False)
        assert hasattr(p, "set_steps")
        assert callable(p.set_steps)

    def test_pipeline_has_add_state_method(self):
        """Pipeline should have add_state method (Phase 2 API)."""
        p = Pipeline(verbose=False)
        assert hasattr(p, "add_state")
        assert callable(p.add_state)

    def test_basic_pipeline_execution(self):
        """Basic pipeline execution should work as before."""
        def step_func(data):
            return {"result": "success", "input": data}

        pipeline = Pipeline(verbose=False)
        pipeline.set_steps([
            (step_func, "test_step", "v1.0"),
        ])

        result = pipeline.run({"test": "data"})
        assert result is not None
        assert "result" in result
        assert result["result"] == "success"


# ============================================================
# Condition API Stability Tests
# ============================================================

class TestConditionAPIStability:
    """Ensure Condition API remains stable."""

    def test_condition_can_instantiate(self):
        """Condition should instantiate without error."""
        def branch_true(data):
            return {"branch": "true"}

        def branch_false(data):
            return {"branch": "false"}

        cond = Condition(
            expression="value > 50",
            branch_true=[(branch_true, "True", "v1.0")],
            branch_false=[(branch_false, "False", "v1.0")],
        )
        assert cond is not None

    def test_condition_has_required_attributes(self):
        """Condition should have required attributes."""
        def branch_true(data):
            return {"branch": "true"}

        cond = Condition(
            expression="value > 50",
            branch_true=[(branch_true, "True", "v1.0")],
        )
        assert hasattr(cond, "expression")
        assert hasattr(cond, "branch_true")


# ============================================================
# Decorator API Stability Tests
# ============================================================

class TestDecoratorAPIStability:
    """Ensure decorator API remains stable."""

    def test_step_decorator_basic_usage(self):
        """step decorator should work with basic usage."""
        @step(description="Test step")
        def test_step(context):
            return {"result": "ok"}

        assert test_step is not None

    def test_step_decorator_with_params(self):
        """step decorator should accept all parameters."""
        @step(
            description="Test step",
            timeout=30,
            tags=["test"],
            depends_on=[],
        )
        def test_step(context):
            return {"result": "ok"}

        assert test_step is not None

    def test_step_registry_is_consistent(self):
        """Step registry should be accessible consistently."""
        registry1 = get_step_registry()
        registry2 = get_step_registry()
        # Both should be StepRegistry instances
        assert isinstance(registry1, StepRegistry)
        assert isinstance(registry2, StepRegistry)


# ============================================================
# Parallel API Stability Tests
# ============================================================

class TestParallelAPIStability:
    """Ensure Parallel API remains stable."""

    def test_execution_mode_values(self):
        """ExecutionMode should have expected values."""
        assert hasattr(ExecutionMode, "IO_BOUND")
        assert hasattr(ExecutionMode, "CPU_BOUND")
        assert hasattr(ExecutionMode, "SEQUENTIAL")

    def test_parallel_executor_can_instantiate(self):
        """ParallelExecutor should instantiate without error."""
        executor = ParallelExecutor(max_workers=2)
        assert executor is not None

    def test_dag_scheduler_can_instantiate(self):
        """DAGScheduler should instantiate without error."""
        scheduler = DAGScheduler()
        assert scheduler is not None


# ============================================================
# Composition API Stability Tests
# ============================================================

class TestCompositionAPIStability:
    """Ensure Composition API remains stable."""

    def test_nested_pipeline_step_can_instantiate(self):
        """NestedPipelineStep should instantiate without error."""
        inner_pipeline = Pipeline(verbose=False)
        step = NestedPipelineStep("test", inner_pipeline)
        assert step is not None

    def test_composition_helper_exists(self):
        """CompositionHelper should exist and be a class."""
        assert isinstance(CompositionHelper, type)


# ============================================================
# Transform Decorator Stability Tests
# ============================================================

class TestTransformDecoratorStability:
    """Ensure transform decorators remain stable."""

    def test_to_obj_is_callable(self):
        """to_obj should be callable."""
        assert callable(to_obj)

    def test_auto_dict_input_is_callable(self):
        """auto_dict_input should be callable."""
        assert callable(auto_dict_input)

    def test_state_is_callable(self):
        """state should be callable."""
        assert callable(state)

    def test_object_to_dict_is_callable(self):
        """object_to_dict should be callable."""
        assert callable(object_to_dict)


# ============================================================
# Tracking API Stability Tests
# ============================================================

class TestTrackingAPIStability:
    """Ensure Tracking API remains stable."""

    def test_severity_values(self):
        """Severity should have expected values."""
        assert hasattr(Severity, "INFO")
        assert hasattr(Severity, "WARNING")
        assert hasattr(Severity, "CRITICAL")

    def test_metric_has_expected_constants(self):
        """Metric should have expected constant attributes."""
        assert hasattr(Metric, "ERROR_RATE")
        assert hasattr(Metric, "PIPELINE_DURATION")
        assert hasattr(Metric, "STEP_DURATION")


# ============================================================
# Async Pipeline Stability Tests
# ============================================================

class TestAsyncPipelineStability:
    """Ensure Async Pipeline API remains stable."""

    def test_pipeline_async_is_class(self):
        """PipelineAsync should be a class."""
        assert isinstance(PipelineAsync, type)

    def test_pipeline_async_importable(self):
        """PipelineAsync should be importable from public API."""
        from wpipe.pipe.pipe_async import PipelineAsync as PASync
        assert isinstance(PASync, type)


# ============================================================
# Module Structure Stability Tests
# ============================================================

class TestModuleStructureStability:
    """Ensure module structure remains stable."""

    def test_wpipe_has_all_attribute(self):
        """wpipe should have __all__ defined."""
        assert hasattr(wpipe, "__all__")
        assert isinstance(wpipe.__all__, list)

    def test_all_exports_are_importable(self):
        """All items in __all__ should be importable."""
        for name in wpipe.__all__:
            # Skip 'start_dashboard' which is lazy-loaded
            if name == "start_dashboard":
                continue
            assert hasattr(wpipe, name), f"{name} should be accessible from wpipe"

    def test_no_duplicate_exports(self):
        """No duplicate exports in __all__."""
        all_list = wpipe.__all__
        assert len(all_list) == len(set(all_list)), "Duplicate exports found in __all__"


# ============================================================
# Error Code Stability Tests
# ============================================================

class TestErrorCodeStability:
    """Ensure error codes remain stable."""

    def test_task_error_exception(self):
        """TaskError should be importable from exception module."""
        from wpipe.exception.api_error import TaskError
        assert issubclass(TaskError, Exception)

    def test_api_error_exception(self):
        """ApiError should be importable from exception module."""
        from wpipe.exception.api_error import ApiError
        assert issubclass(ApiError, Exception)

    def test_process_error_exception(self):
        """ProcessError should be importable from exception module."""
        from wpipe.exception.api_error import ProcessError
        assert issubclass(ProcessError, Exception)

    def test_codes_constant_exists(self):
        """Codes constant should exist in exception module."""
        from wpipe.exception.api_error import Codes
        assert Codes is not None


# ============================================================
# Integration Point Stability Tests
# ============================================================

class TestIntegrationPointStability:
    """Ensure integration points remain stable."""

    def test_wsqlite_context_manager(self):
        """Wsqlite should work as context manager."""
        import tempfile
        import os

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_regression.db")
            from wpipe.sqlite import Wsqlite as WsqliteCls
            db = WsqliteCls(db_name=db_path)
            assert db is not None
            assert hasattr(db, "__enter__")
            assert hasattr(db, "__exit__")

    def test_new_logger_returns_logger(self):
        """new_logger should return a logger instance."""
        logger = new_logger("test_regression")
        assert logger is not None
        assert hasattr(logger, "info")
        assert hasattr(logger, "error")
        assert hasattr(logger, "warning")
