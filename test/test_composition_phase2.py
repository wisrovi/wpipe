"""
Tests for Phase 2 composition features.
"""

import pytest

from wpipe.composition import CompositionHelper, NestedPipelineStep, PipelineAsStep


class TestCompositionHelper:
    """Test pipeline composition utilities."""

    def test_merge_contexts_child_wins(self):
        """Test context merging with child_wins strategy."""
        parent = {"key1": "parent_value", "key2": "shared"}
        child = {"key2": "child_value", "key3": "new"}

        merged = CompositionHelper.merge_contexts(parent, child, "child_wins")

        assert merged["key1"] == "parent_value"
        assert merged["key2"] == "child_value"
        assert merged["key3"] == "new"

    def test_merge_contexts_parent_wins(self):
        """Test context merging with parent_wins strategy."""
        parent = {"key1": "parent_value", "key2": "shared"}
        child = {"key2": "child_value", "key3": "new"}

        merged = CompositionHelper.merge_contexts(parent, child, "parent_wins")

        assert merged["key1"] == "parent_value"
        assert merged["key2"] == "shared"
        assert merged["key3"] == "new"

    def test_merge_contexts_merge_list(self):
        """Test context merging with list merging."""
        parent = {"items": [1, 2, 3], "name": "parent"}
        child = {"items": [4, 5], "name": "child"}

        merged = CompositionHelper.merge_contexts(parent, child, "merge_list")

        assert merged["items"] == [1, 2, 3, 4, 5]
        assert merged["name"] == "child"

    def test_extract_context_subset(self):
        """Test extracting context subset."""
        context = {"key1": "value1", "key2": "value2", "key3": "value3"}

        subset = CompositionHelper.extract_context_subset(context, ["key1", "key3"])

        assert subset == {"key1": "value1", "key3": "value3"}
        assert "key2" not in subset

    def test_validate_context_compatibility_valid(self):
        """Test validating compatible contexts."""
        parent_schema = {"id": int, "name": str}
        child_schema = {"id": int, "name": str}

        assert CompositionHelper.validate_context_compatibility(
            parent_schema, child_schema
        )

    def test_validate_context_compatibility_invalid(self):
        """Test validating incompatible contexts."""
        parent_schema = {"id": int, "name": str}
        child_schema = {"id": str, "name": str}  # Wrong type

        with pytest.raises(TypeError):
            CompositionHelper.validate_context_compatibility(
                parent_schema, child_schema
            )


class TestNestedPipelineStep:
    """Test nested pipeline steps."""

    def test_basic_nesting(self):
        """Test basic pipeline nesting."""
        from wpipe import Pipeline

        # Create sub-pipeline
        sub_pipeline = Pipeline()
        sub_pipeline.add_state("step_1", lambda c: {"sub_result": 42})

        # Create nested step
        nested = NestedPipelineStep("nested", sub_pipeline)

        # Execute
        result = nested.run({})

        assert result["sub_result"] == 42

    def test_context_filtering(self):
        """Test context filtering."""
        from wpipe import Pipeline

        # Create sub-pipeline
        sub_pipeline = Pipeline()
        sub_pipeline.add_state("step_1", lambda c: {"result": c.get("input") * 2})

        # Context filter
        def filter_context(context):
            return {"input": 21}

        # Create nested step with filter
        nested = NestedPipelineStep(
            "nested",
            sub_pipeline,
            context_filter=filter_context,
        )

        # Execute with empty context
        result = nested.run({"ignored": "value"})

        assert result["result"] == 42

    def test_result_filtering(self):
        """Test result filtering."""
        from wpipe import Pipeline

        # Create sub-pipeline
        sub_pipeline = Pipeline()
        sub_pipeline.add_state(
            "step_1",
            lambda c: {
                "public_result": 100,
                "internal_data": "secret",
            },
        )

        # Result filter
        def filter_result(result):
            return {k: v for k, v in result.items() if not k.startswith("internal")}

        # Create nested step with filter
        nested = NestedPipelineStep(
            "nested",
            sub_pipeline,
            result_filter=filter_result,
        )

        # Execute
        result = nested.run({})

        assert result["public_result"] == 100
        assert "internal_data" not in result

    def test_execution_timing(self):
        """Test execution time tracking."""
        import time

        from wpipe import Pipeline

        # Create sub-pipeline with delay
        sub_pipeline = Pipeline()
        sub_pipeline.add_state("step_1", lambda c: (time.sleep(0.1), {"done": True})[1])

        # Create nested step
        nested = NestedPipelineStep("nested", sub_pipeline)

        # Execute
        nested.run({})

        # Check timing
        exec_time = nested.get_execution_time()
        assert exec_time >= 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
