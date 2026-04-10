"""
Tests for Phase 2 decorator features.
"""

import pytest

from wpipe.decorators import (
    AutoRegister,
    StepRegistry,
    clear_registry,
    get_step_registry,
    step,
)


class TestStepDecorator:
    """Test @step decorator."""

    def setup_method(self):
        """Clear registry before each test."""
        clear_registry()

    def test_basic_decoration(self):
        """Test basic step decoration."""

        @step(name="my_step", description="Test step")
        def my_function(context):
            return {"result": 42}

        # Check that function is callable
        result = my_function({})
        assert result["result"] == 42

    def test_decorator_metadata(self):
        """Test decorator metadata attachment."""

        @step(
            name="test_step",
            timeout=30,
            description="Test description",
            tags=["important", "test"],
        )
        def decorated_func(context):
            return {}

        # Check metadata
        assert hasattr(decorated_func, "_wpipe_metadata")
        metadata = decorated_func._wpipe_metadata

        assert metadata.name == "test_step"
        assert metadata.timeout == 30
        assert metadata.description == "Test description"
        assert "important" in metadata.tags

    def test_decorator_registry(self):
        """Test decorator registration."""

        @step(name="step_1")
        def func_1(context):
            return {}

        @step(name="step_2", depends_on=["step_1"])
        def func_2(context):
            return {}

        # Check registry
        registry = get_step_registry()

        assert "step_1" in registry.get_all()
        assert "step_2" in registry.get_all()

        step_2_meta = registry.get("step_2").get_metadata()
        assert "step_1" in step_2_meta.depends_on

    def test_decorator_with_dependencies(self):
        """Test decorator with dependencies."""

        @step(name="fetch", description="Fetch data")
        def fetch_data(context):
            return {"data": [1, 2, 3]}

        @step(
            name="process",
            depends_on=["fetch"],
            description="Process data",
        )
        def process_data(context):
            return {"processed": len(context["data"])}

        # Check dependencies
        registry = get_step_registry()
        process_meta = registry.get("process").get_metadata()

        assert "fetch" in process_meta.depends_on


class TestStepRegistry:
    """Test step registry functionality."""

    def setup_method(self):
        """Clear registry before each test."""
        clear_registry()

    def test_registry_registration(self):
        """Test manual registry registration."""
        registry = StepRegistry()

        def my_step(context):
            return {}

        registry.register_func(my_step, name="test_step", timeout=30)

        assert registry.get("test_step") is not None

    def test_registry_get_all(self):
        """Test getting all steps from registry."""
        registry = StepRegistry()

        registry.register_func(lambda c: {}, name="step_1")
        registry.register_func(lambda c: {}, name="step_2")
        registry.register_func(lambda c: {}, name="step_3")

        all_steps = registry.get_all()

        assert len(all_steps) == 3
        assert "step_1" in all_steps
        assert "step_2" in all_steps
        assert "step_3" in all_steps

    def test_registry_clear(self):
        """Test clearing registry."""
        registry = StepRegistry()

        registry.register_func(lambda c: {}, name="step_1")
        assert len(registry.get_all()) == 1

        registry.clear()
        assert len(registry.get_all()) == 0


class TestAutoRegister:
    """Test auto-registration functionality."""

    def setup_method(self):
        """Clear registry before each test."""
        clear_registry()

    def test_auto_register_all(self):
        """Test auto-registering all steps to pipeline."""
        from wpipe import Pipeline

        @step(name="step_1")
        def func_1(context):
            return {"value": 1}

        @step(name="step_2", depends_on=["step_1"])
        def func_2(context):
            return {"value": context["value"] + 1}

        # Create pipeline
        pipeline = Pipeline()

        # Auto-register
        registry = get_step_registry()
        AutoRegister.register_all(pipeline, registry)

        # Check that steps are registered
        assert len(pipeline.steps) == 2

    def test_auto_register_by_tag(self):
        """Test auto-registering by tag."""
        from wpipe import Pipeline

        @step(name="step_1", tags=["important", "data"])
        def func_1(context):
            return {}

        @step(name="step_2", tags=["optional", "data"])
        def func_2(context):
            return {}

        @step(name="step_3", tags=["important", "processing"])
        def func_3(context):
            return {}

        # Create pipelines
        data_pipeline = Pipeline()
        important_pipeline = Pipeline()

        registry = get_step_registry()

        # Register by tag
        AutoRegister.register_by_tag(data_pipeline, "data", registry)
        AutoRegister.register_by_tag(important_pipeline, "important", registry)

        # Check results
        assert len(data_pipeline.steps) == 2
        assert len(important_pipeline.steps) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
